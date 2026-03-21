// 🦞 OpenClaw 像素办公室 - 技能数据

const SKILLS = {
  // v2.0 优化技能
  "travel-planner": {
    name: "旅行规划助手",
    icon: "✈️",
    version: "v2.0",
    category: "生活",
    codeSize: "19KB",
    description: "行程规划、景点推荐、预算估算、打包清单",
    features: [
      "🌍 12 个热门城市数据库",
      "🎯 10 种旅行模板（情侣游/亲子游/背包客等）",
      "🧳 个性化打包清单生成",
      "💡 旅行贴士和注意事项",
      "💰 详细预算估算"
    ],
    commands: [
      "帮我规划 3 天的北京旅行",
      "情侣游去三亚 5 天",
      "去海边要带什么",
      "去拉萨注意事项"
    ]
  },
  
  "habit-tracker": {
    name: "习惯养成助手",
    icon: "🎯",
    version: "v2.0",
    category: "健康",
    codeSize: "19KB",
    description: "习惯打卡、统计分析、成就系统",
    features: [
      "📚 20+ 习惯模板库（5 大类）",
      "🏆 10 个成就徽章系统",
      "📊 周/月/年统计报表",
      "⚡ 一键打卡全部习惯",
      "📈 完成率追踪"
    ],
    commands: [
      "我想养成每天读书的习惯",
      "打卡读书",
      "打卡全部",
      "查看习惯统计",
      "查看我的成就"
    ]
  },
  
  "goal-manager": {
    name: "目标管理助手",
    icon: "🎯",
    version: "v2.0",
    category: "工作",
    codeSize: "19KB",
    description: "目标设定、SMART/OKR 框架、进度跟踪",
    features: [
      "📋 13 个目标模板（SMART/OKR）",
      "📐 双框架支持",
      "📝 5 种复盘模板（日/周/月/季/年）",
      "📊 可视化进度追踪",
      "🎯 目标分解"
    ],
    commands: [
      "创建阅读计划目标",
      "创建职业晋升目标",
      "更新减肥塑形 KR1 为 5",
      "做月度复盘",
      "有哪些目标模板"
    ]
  },
  
  "expense-tracker": {
    name: "记账助手",
    icon: "💰",
    version: "v2.0",
    category: "生活",
    codeSize: "18KB",
    description: "记账、分类统计、预算管理、储蓄目标",
    features: [
      "📊 10 大类 20+ 子分类",
      "💰 分类预算 + 超支预警",
      "🎯 6 个储蓄目标模板",
      "🔍 消费分析 + 省钱建议",
      "📈 收支统计报表"
    ],
    commands: [
      "今天花了 50 元吃饭",
      "这个月花了多少钱",
      "设置每月预算 5000 元",
      "创建应急基金",
      "消费分析"
    ]
  },
  
  // 其他技能（部分示例）
  "email-helper": {
    name: "邮件助手",
    icon: "📧",
    version: "v2.0",
    category: "工作",
    codeSize: "11KB",
    description: "8 种邮件模板、中英文支持、邮件润色",
    features: [
      "请假/汇报/会议/商务/求职/感谢/道歉/催款",
      "中英文双语支持",
      "邮件润色功能"
    ],
    commands: ["帮我写一封请假邮件"]
  },
  
  "calendar-manager": {
    name: "日历管理",
    icon: "📅",
    version: "v2.0",
    category: "工作",
    codeSize: "13KB",
    description: "中国节日查询、纪念日管理、倒计时",
    features: [
      "中国节日查询",
      "纪念日管理",
      "倒计时功能",
      "时间统计"
    ],
    commands: ["距离春节还有多少天"]
  },
  
  "recipe-finder": {
    name: "菜谱 finder",
    icon: "🍳",
    version: "v2.0",
    category: "生活",
    codeSize: "15KB",
    description: "12 道菜谱、营养分析、购物清单",
    features: [
      "12 道菜谱（家常菜/汤类/素食/快手菜）",
      "营养分析（热量/蛋白质）",
      "购物清单生成",
      "难度筛选"
    ],
    commands: ["我想做一道家常菜"]
  },
  
  "stock-watcher": {
    name: "股票观察",
    icon: "📈",
    version: "v2.0",
    category: "财务",
    codeSize: "14KB",
    description: "13 只股票、板块查询、价格提醒",
    features: [
      "13 只股票（A 股/港股/美股）",
      "板块查询（白酒/新能源/科技/金融/互联网）",
      "价格提醒",
      "市场摘要"
    ],
    commands: ["茅台股价多少"]
  },
  
  "book-recommender": {
    name: "书籍推荐",
    icon: "📚",
    version: "v2.0",
    category: "学习",
    codeSize: "17KB",
    description: "20 本书、心情推荐、书架管理",
    features: [
      "20 本书（小说/商业/成长/历史/科幻/推理）",
      "心情推荐（迷茫/焦虑/低落/兴奋/平静）",
      "书架管理（想读/在读/已读）",
      "阅读统计"
    ],
    commands: ["我最近很迷茫，推荐一本书"]
  },
  
  "meeting-assistant": {
    name: "会议助手",
    icon: "📋",
    version: "v2.0",
    category: "工作",
    codeSize: "15KB",
    description: "会议模板、智能纪要、待办提取",
    features: [
      "会议模板（周会/项目启动/评审会/头脑风暴）",
      "智能会议纪要生成",
      "待办事项自动提取",
      "会议统计"
    ],
    commands: ["帮我生成会议纪要"]
  },
  
  "movie-recommender": {
    name: "电影推荐",
    icon: "🎬",
    version: "v1.0",
    category: "娱乐",
    codeSize: "8KB",
    description: "豆瓣电影推荐、类型筛选",
    features: [
      "豆瓣 API 对接",
      "类型筛选",
      "评分排序"
    ],
    commands: ["推荐一部高分电影"]
  },
  
  "music-helper": {
    name: "音乐助手",
    icon: "🎵",
    category: "娱乐",
    version: "v1.0",
    codeSize: "7KB",
    description: "网易云音乐推荐、歌单管理",
    features: [
      "网易云 API 对接",
      "歌单推荐",
      "歌词显示"
    ],
    commands: ["推荐一首歌"]
  },
  
  "price-tracker": {
    name: "价格监控",
    icon: "🏷️",
    version: "v1.0",
    category: "购物",
    codeSize: "9KB",
    description: "电商价格监控、降价提醒",
    features: [
      "电商爬虫",
      "价格历史",
      "降价提醒"
    ],
    commands: ["监控这个商品的价格"]
  },
  
  "weather": {
    name: "天气查询",
    icon: "🌤️",
    version: "v1.0",
    category: "生活",
    codeSize: "5KB",
    description: "实时天气、天气预报",
    features: [
      "实时天气",
      "7 天预报",
      "多城市支持"
    ],
    commands: ["北京天气怎么样"]
  },
  
  "news-digest": {
    name: "新闻摘要",
    icon: "📰",
    version: "v1.0",
    category: "资讯",
    codeSize: "6KB",
    description: "新闻聚合、智能摘要",
    features: [
      "多源新闻聚合",
      "智能摘要",
      "分类浏览"
    ],
    commands: ["今天的新闻摘要"]
  },
  
  "ppt-generator": {
    name: "PPT 生成",
    icon: "📊",
    version: "v1.0",
    category: "工作",
    codeSize: "10KB",
    description: "PPT 模板、自动生成",
    features: [
      "多套模板",
      "自动生成",
      "图表支持"
    ],
    commands: ["帮我做一个项目汇报 PPT"]
  },
  
  "quiz-generator": {
    name: "测验生成",
    icon: "❓",
    version: "v1.0",
    category: "学习",
    codeSize: "7KB",
    description: "题库模板、难度分级",
    features: [
      "题库模板",
      "难度分级",
      "答题统计"
    ],
    commands: ["生成一份英语测验"]
  },
  
  "travel-planner-old": {
    name: "旅行规划（旧）",
    icon: "✈️",
    version: "v1.0",
    category: "生活",
    codeSize: "5KB",
    description: "基础行程规划",
    features: [
      "基础行程规划",
      "简单预算"
    ],
    commands: ["规划北京旅行"]
  }
};

// 分类映射
const CATEGORIES = {
  "生活": ["travel-planner", "expense-tracker", "recipe-finder", "weather"],
  "健康": ["habit-tracker"],
  "工作": ["goal-manager", "email-helper", "calendar-manager", "meeting-assistant", "ppt-generator"],
  "学习": ["book-recommender", "quiz-generator"],
  "财务": ["stock-watcher"],
  "娱乐": ["movie-recommender", "music-helper"],
  "购物": ["price-tracker"],
  "资讯": ["news-digest"]
};

// v2.0 技能列表
const V2_SKILLS = ["travel-planner", "habit-tracker", "goal-manager", "expense-tracker", "email-helper", "calendar-manager", "recipe-finder", "stock-watcher", "book-recommender", "meeting-assistant"];

// 模拟实时数据
const MOCK_DATA = {
  todayCheckins: 15,
  goalProgress: 67,
  monthExpense: 3580,
  totalSkills: 43
};
