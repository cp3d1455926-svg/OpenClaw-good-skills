#!/usr/bin/env python3
"""
Skill深度测试脚本
检查所有技能的文档和代码质量
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

class SkillTester:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.report = {
            "test_date": datetime.now().isoformat(),
            "total_skills": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "skills": []
        }
        
        # 需要跳过的文件夹
        self.skip_dirs = {
            '.git', '.openclaw', 'memory', 'ontology', 'promotions', 
            'agent-browser', 'openclaw-pixel-office', 'pixel-office'
        }
    
    def is_skill_folder(self, path):
        """判断是否为技能文件夹"""
        if not path.is_dir():
            return False
        if path.name.startswith('.'):
            return False
        if path.name in self.skip_dirs:
            return False
        # 检查是否有SKILL.md
        return (path / 'SKILL.md').exists()
    
    def check_skill_md(self, skill_path):
        """检查SKILL.md"""
        skill_md = skill_path / 'SKILL.md'
        issues = []
        warnings = []
        
        if not skill_md.exists():
            issues.append("缺少SKILL.md")
            return {"issues": issues, "warnings": warnings}
        
        content = skill_md.read_text(encoding='utf-8')
        
        # 检查关键部分
        checks = {
            '标题': r'^#\s+.+',
            '功能描述': r'##\s*功能|功能描述|Features',
            '使用方法': r'##\s*使用|使用方法|Usage|示例',
            '版本号': r'版本[:：]\s*v?\d+\.\d+',
            '作者': r'作者[:：]|Author'
        }
        
        for check_name, pattern in checks.items():
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                if check_name in ['版本号', '作者']:
                    warnings.append(f"缺少{check_name}")
                else:
                    issues.append(f"缺少{check_name}")
        
        # 检查文件大小
        if skill_md.stat().st_size < 500:
            warnings.append("SKILL.md内容较少")
        
        return {"issues": issues, "warnings": warnings}
    
    def check_code_files(self, skill_path):
        """检查代码文件"""
        issues = []
        warnings = []
        
        # 查找Python文件
        py_files = list(skill_path.glob('*.py'))
        
        if not py_files:
            # 检查是否有其他类型的代码文件
            other_files = list(skill_path.glob('*.js')) + list(skill_path.glob('*.sh'))
            if not other_files:
                warnings.append("没有找到代码文件")
        else:
            # 检查Python文件质量
            for py_file in py_files:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                
                # 检查是否有敏感信息
                sensitive_patterns = [
                    r'api[_-]?key\s*=\s*["\']\w+',
                    r'password\s*=\s*["\']\w+',
                    r'secret\s*=\s*["\']\w+',
                    r'token\s*=\s*["\']\w+',
                ]
                
                for pattern in sensitive_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append(f"{py_file.name}可能包含敏感信息")
                        break
                
                # 检查文件大小
                if py_file.stat().st_size > 100000:  # 100KB
                    warnings.append(f"{py_file.name}文件较大({py_file.stat().st_size//1024}KB)")
        
        return {"issues": issues, "warnings": warnings}
    
    def check_readme(self, skill_path):
        """检查README.md"""
        readme = skill_path / 'README.md'
        if not readme.exists():
            return {"issues": [], "warnings": ["缺少README.md"]}
        return {"issues": [], "warnings": []}
    
    def test_skill(self, skill_path):
        """测试单个技能"""
        skill_name = skill_path.name
        
        result = {
            "name": skill_name,
            "path": str(skill_path),
            "status": "passed",
            "issues": [],
            "warnings": [],
            "details": {}
        }
        
        # 检查SKILL.md
        md_check = self.check_skill_md(skill_path)
        result["issues"].extend(md_check["issues"])
        result["warnings"].extend(md_check["warnings"])
        
        # 检查代码文件
        code_check = self.check_code_files(skill_path)
        result["issues"].extend(code_check["issues"])
        result["warnings"].extend(code_check["warnings"])
        
        # 检查README
        readme_check = self.check_readme(skill_path)
        result["warnings"].extend(readme_check["warnings"])
        
        # 统计文件
        result["details"]["files"] = len(list(skill_path.iterdir()))
        
        # 确定状态
        if result["issues"]:
            result["status"] = "failed"
            self.report["failed"] += 1
        elif result["warnings"]:
            result["status"] = "warning"
            self.report["warnings"] += 1
        else:
            self.report["passed"] += 1
        
        return result
    
    def run_tests(self):
        """运行所有测试"""
        print("开始深度测试所有技能...\n")
        
        # 扫描技能文件夹
        skill_folders = [p for p in self.base_path.iterdir() if self.is_skill_folder(p)]
        
        # 添加workspace/skills中的技能
        workspace_skills = Path(r"C:\Users\shenz\.openclaw\workspace\skills")
        if workspace_skills.exists():
            for p in workspace_skills.iterdir():
                if self.is_skill_folder(p):
                    skill_folders.append(p)
        
        self.report["total_skills"] = len(skill_folders)
        
        print(f"发现 {len(skill_folders)} 个技能文件夹\n")
        
        for i, skill_path in enumerate(sorted(skill_folders, key=lambda x: x.name), 1):
            print(f"[{i}/{len(skill_folders)}] 测试: {skill_path.name}...", end=" ")
            result = self.test_skill(skill_path)
            self.report["skills"].append(result)
            
            if result["status"] == "passed":
                print("[OK]")
            elif result["status"] == "warning":
                print(f"[WARN] ({len(result['warnings'])} warnings)")
            else:
                print(f"[FAIL] ({len(result['issues'])} issues)")
        
        return self.report
    
    def generate_report(self):
        """生成测试报告"""
        report_lines = [
            "# Skills 深度测试报告",
            f"**测试日期**: {self.report['test_date']}",
            f"**测试技能数**: {self.report['total_skills']}",
            "",
            "## 统计概览",
            "",
            f"- [OK] 通过: {self.report['passed']}",
            f"- [WARN] 警告: {self.report['warnings']}",
            f"- [FAIL] 失败: {self.report['failed']}",
            f"- 通过率: {(self.report['passed'] / self.report['total_skills'] * 100):.1f}%",
            "",
            "## 详细结果",
            "",
        ]
        
        # 按状态分组
        failed = [s for s in self.report["skills"] if s["status"] == "failed"]
        warnings = [s for s in self.report["skills"] if s["status"] == "warning"]
        passed = [s for s in self.report["skills"] if s["status"] == "passed"]
        
        if failed:
            report_lines.extend(["### 失败的技能", ""])
            for skill in failed:
                report_lines.append(f"#### {skill['name']}")
                for issue in skill["issues"]:
                    report_lines.append(f"- [FAIL] {issue}")
                if skill["warnings"]:
                    for warning in skill["warnings"]:
                        report_lines.append(f"- [WARN] {warning}")
                report_lines.append("")
        
        if warnings:
            report_lines.extend(["### 有警告的技能", ""])
            for skill in warnings:
                report_lines.append(f"#### {skill['name']}")
                for warning in skill["warnings"]:
                    report_lines.append(f"- [WARN] {warning}")
                report_lines.append("")
        
        if passed:
            report_lines.extend(["### 通过的技能", ""])
            for skill in passed:
                report_lines.append(f"- [OK] {skill['name']}")
            report_lines.append("")
        
        return "\n".join(report_lines)

if __name__ == "__main__":
    # 测试OpenClaw-good-skill文件夹
    tester = SkillTester(r"C:\Users\shenz\.openclaw\workspace\OpenClaw-good-skill")
    report = tester.run_tests()
    
    # 生成报告
    report_md = tester.generate_report()
    
    # 保存报告
    report_path = r"C:\Users\shenz\.openclaw\workspace\SKILL_DEEP_TEST_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_md)
    
    print(f"\n✅ 测试完成！报告已保存到: {report_path}")
    print(f"\n统计: {report['passed']}通过, {report['warnings']}警告, {report['failed']}失败")
