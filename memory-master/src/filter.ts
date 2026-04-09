/**
 * Memory-Master 敏感数据过滤模块
 * 
 * 支持 16 种敏感数据类型检测
 * 基于 Anthropic 安全最佳实践
 */

/**
 * 敏感数据类型
 */
export type SensitiveType =
  | 'api_key'
  | 'password'
  | 'credit_card'
  | 'id_card'
  | 'phone'
  | 'email'
  | 'bank_card'
  | 'address'
  | 'private_key'
  | 'database_url'
  | 'aws_key'
  | 'github_token'
  | 'openai_key'
  | 'anthropic_key'
  | 'aliyun_key'
  | 'other';

/**
 * 检测结果
 */
export interface DetectedSensitive {
  type: SensitiveType;
  value: string;        // 脱敏后的值
  position: number;     // 位置
  original: string;     // 原始值（用于内部处理）
}

/**
 * 过滤结果
 */
export interface FilterResult {
  hasSensitive: boolean;
  filtered: string;     // 过滤后的内容
  detected: DetectedSensitive[];
}

/**
 * 敏感数据检测规则
 */
interface DetectionRule {
  type: SensitiveType;
  pattern: RegExp;
  mask: string;         // 脱敏标记
}

/**
 * 检测规则列表
 */
const DETECTION_RULES: DetectionRule[] = [
  // API Keys
  { type: 'github_token', pattern: /ghp_[a-zA-Z0-9]{36}/g, mask: '[GITHUB_TOKEN]' },
  { type: 'openai_key', pattern: /sk-[a-zA-Z0-9]{48}/g, mask: '[OPENAI_KEY]' },
  { type: 'anthropic_key', pattern: /sk-ant-[a-zA-Z0-9]{95}/g, mask: '[ANTHROPIC_KEY]' },
  { type: 'aws_key', pattern: /AKIA[0-9A-Z]{16}/g, mask: '[AWS_KEY]' },
  { type: 'aliyun_key', pattern: /LTAI[a-zA-Z0-9]{12,20}/g, mask: '[ALIYUN_KEY]' },
  { type: 'api_key', pattern: /api[_-]?key\s*[=:]\s*["']?[a-zA-Z0-9]{16,}["']?/gi, mask: '[API_KEY]' },
  
  // 密码
  { type: 'password', pattern: /密码\s*[=:]\s*["']?[^\s"']{4,}["']?/gi, mask: '[PASSWORD]' },
  { type: 'private_key', pattern: /-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----[\s\S]*?-----END (RSA |EC |DSA )?PRIVATE KEY-----/g, mask: '[PRIVATE_KEY]' },
  
  // 数据库连接
  { type: 'database_url', pattern: /(mongodb|mysql|postgresql|redis):\/\/[^\s]+/gi, mask: '[DATABASE_URL]' },
  
  // 信用卡
  { type: 'credit_card', pattern: /\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b/g, mask: '[CREDIT_CARD]' },
  
  // 身份证号
  { type: 'id_card', pattern: /\b[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b/g, mask: '[ID_CARD]' },
  
  // 手机号
  { type: 'phone', pattern: /\b1[3-9]\d{9}\b/g, mask: '[PHONE]' },
  
  // 邮箱
  { type: 'email', pattern: /\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b/g, mask: '[EMAIL]' },
  
  // 银行卡号
  { type: 'bank_card', pattern: /\b[2-6]\d{15,18}\b/g, mask: '[BANK_CARD]' },
  
  // 地址（简单匹配）
  { type: 'address', pattern: /[省市县][^\s]{2,20}[路街道][^\s]{2,20}[号栋楼]/g, mask: '[ADDRESS]' },
];

/**
 * 过滤敏感数据
 */
export async function filterSensitiveData(content: string): Promise<FilterResult> {
  const detected: DetectedSensitive[] = [];
  let filtered = content;

  // 遍历所有检测规则
  for (const rule of DETECTION_RULES) {
    const matches = filtered.matchAll(rule.pattern);
    
    for (const match of matches) {
      const original = match[0];
      const position = match.index || 0;
      
      // 脱敏处理（保留部分信息用于识别）
      const masked = maskValue(original, rule.type);
      
      detected.push({
        type: rule.type,
        value: masked,
        position,
        original,
      });
      
      // 替换为脱敏标记
      filtered = filtered.replace(original, rule.mask);
    }
  }

  return {
    hasSensitive: detected.length > 0,
    filtered,
    detected: detected.map(item => ({
      ...item,
      value: maskValue(item.original, item.type),
    })),
  };
}

/**
 * 脱敏处理
 */
function maskValue(value: string, type: SensitiveType): string {
  const visible = Math.max(2, Math.floor(value.length * 0.2)); // 显示 20%
  const masked = value.length - visible;
  
  return value.substring(0, visible) + '*'.repeat(masked);
}

/**
 * 检测敏感数据（不替换）
 */
export async function detectSensitiveData(content: string): Promise<DetectedSensitive[]> {
  const result = await filterSensitiveData(content);
  return result.detected;
}

/**
 * 测试用例
 */
export async function runFilterTests(): Promise<void> {
  const tests = [
    { input: '我的密码是 123456', expected: true },
    { input: 'GitHub Token: ghp_abcdefghijklmnopqrstuvwxyz0123456789', expected: true },
    { input: 'OpenAI Key: sk-abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnop', expected: true },
    { input: '手机号：13812345678', expected: true },
    { input: '邮箱：test@example.com', expected: true },
    { input: '我喜欢吃川菜', expected: false },
    { input: '每天早上 7 点起床', expected: false },
  ];

  console.log('🧪 敏感数据过滤测试');
  console.log('==================\n');

  let passed = 0;
  for (const test of tests) {
    const result = await filterSensitiveData(test.input);
    const success = result.hasSensitive === test.expected;
    
    if (success) {
      console.log(`✅ ${test.input.substring(0, 30)}...`);
      passed++;
    } else {
      console.log(`❌ ${test.input.substring(0, 30)}...`);
      console.log(`   期望：${test.expected}, 实际：${result.hasSensitive}`);
    }
  }

  console.log(`\n📊 测试结果：${passed}/${tests.length} 通过`);
  
  if (passed === tests.length) {
    console.log('🎉 全部通过！');
  }
}

// 导出
export default {
  filterSensitiveData,
  detectSensitiveData,
  runFilterTests,
};
