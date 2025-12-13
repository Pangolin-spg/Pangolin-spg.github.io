# Elementor Form 字段配置指南

## 字段配置列表

### 1. Company Name (公司名称)
- **Type**: Text
- **Label**: Company Name
- **Placeholder**: Enter your company name
- **Required**: Yes
- **Field ID**: company_name
- **Width**: 100%

### 2. Work Email (工作邮箱)
- **Type**: Email
- **Label**: Work Email
- **Placeholder**: your.email@company.com
- **Required**: Yes
- **Field ID**: work_email
- **Width**: 100%
- **Help Text**: We'll use this to send you the interview link

### 3. Your Role / Position (职位)
- **Type**: Text
- **Label**: Your Role / Position
- **Placeholder**: e.g., Product Manager, Data Analyst
- **Required**: Yes
- **Field ID**: position
- **Width**: 100%

### 4. Current Data Needs (数据需求)
- **Type**: Textarea
- **Label**: Current Data Needs
- **Placeholder**: Tell us about your current data collection requirements...
- **Required**: Yes
- **Field ID**: current_needs
- **Rows**: 3
- **Width**: 100%

### 5. Current Pain Points (当前痛点)
- **Type**: Textarea
- **Label**: Current Pain Points
- **Placeholder**: What challenges are you facing with your current solution?
- **Required**: Yes
- **Field ID**: pain_points
- **Rows**: 3
- **Width**: 100%

---

## Form Actions 配置

### Action 1: Email (发送邮件)

**基本设置**:
- **To**: your-email@example.com (替换为您的邮箱)
- **Subject**: New Interview Application - [field id="company_name"]
- **From Email**: [field id="work_email"]
- **From Name**: [field id="company_name"]
- **Reply To**: [field id="work_email"]

**Message (邮件内容模板)**:
```
New Interview Application Received
=====================================

Company Information:
- Company Name: [field id="company_name"]
- Contact Email: [field id="work_email"]
- Position: [field id="position"]

Business Details:
- Current Data Needs: 
[field id="current_needs"]

- Current Pain Points:
[field id="pain_points"]

=====================================
Submitted at: [date] [time]
IP Address: [remote_ip]

Next Steps:
1. Review the application
2. Schedule interview via: https://calendly.com/tammy-pangolinfo/customer-interview
```

**Additional Options**:
- **Email Content Type**: HTML (可选,如果想要更美观的邮件)
- **Send Copy to Applicant**: Yes (可选,发送确认邮件给申请人)

### Action 2: Redirect (提交后跳转)

**设置**:
- **Redirect To**: Custom URL
- **URL**: https://calendly.com/tammy-pangolinfo/customer-interview

或者使用 **Success Message** 显示成功消息,然后手动添加Calendly链接。

---

## Form 样式设置

### Form Fields (字段样式)
- **Label Color**: #1e293b
- **Label Typography**: 
  - Font Size: 13px
  - Font Weight: 600
- **Field Background**: #ffffff
- **Field Border**: 2px solid #e2e8f0
- **Field Border Radius**: 10px
- **Field Padding**: 10px 14px
- **Field Focus Border Color**: #2563eb

### Button (提交按钮)
- **Text**: Submit Application
- **Background**: Linear Gradient (#2563eb to #7c3aed)
- **Text Color**: #ffffff
- **Typography**:
  - Font Size: 15px
  - Font Weight: 900
- **Border Radius**: 12px
- **Padding**: 14px 32px
- **Width**: Full Width
- **Alignment**: Center
- **Icon**: Arrow Right (可选)

### Spacing (间距)
- **Row Gap**: 16px
- **Column Gap**: 16px

---

## 成功消息配置

### Success Message (提交成功消息)
```html
<div style="text-align: center; padding: 20px;">
    <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;">
        <i class="fas fa-check" style="font-size: 32px; color: white;"></i>
    </div>
    <h3 style="font-size: 22px; font-weight: 900; color: #1e293b; margin-bottom: 10px;">Application Submitted! 🎉</h3>
    <p style="font-size: 14px; color: #64748b; margin-bottom: 20px;">
        Thank you for your interest! Your application has been received.<br>
        Now, let's schedule your interview to unlock your lifetime 50% discount.
    </p>
    <a href="https://calendly.com/tammy-pangolinfo/customer-interview" target="_blank" style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: #1e3a8a; font-size: 15px; font-weight: 900; padding: 12px 28px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 10px;">
        <i class="fas fa-calendar-alt"></i>
        Schedule Interview Now
    </a>
</div>
```

---

## WP Mail SMTP 集成

由于您已经配置了 WP Mail SMTP,Elementor Forms 会自动使用它发送邮件。

**确认 WP Mail SMTP 配置**:
1. 进入 `WP Mail SMTP` → `Settings`
2. 确认邮件发送方式已配置(Gmail, SendGrid, Mailgun等)
3. 发送测试邮件确认正常工作

**Elementor 会自动使用 WP Mail SMTP**,无需额外配置!

---

## 表单验证消息(英文)

在 Elementor Form 的 **Additional Options** 中设置:

- **Required Message**: This field is required
- **Invalid Message**: Please enter a valid value
- **Email Invalid Message**: Please enter a valid email address

---

## 测试清单

- [ ] Banner 显示正常
- [ ] 倒计时工作正常
- [ ] 点击 "Apply Now" 打开弹窗
- [ ] 表单字段验证正常(英文提示)
- [ ] 提交表单后收到邮件
- [ ] 邮件内容完整
- [ ] 成功页面显示正常
- [ ] Calendly 链接可点击
- [ ] 移动端显示正常
