# from IPython.display import display, Markdown
#
# er_diagram_code = """
# ```mermaid
# erDiagram
#     用户信息表 {
#         int id PK "用户ID"
#         varchar name "姓名"
#         char gender "性别"
#         date dateOfBirth "出生日期"
#         varchar password "密码"
#         int isSuperuser "是否管理员"
#     }
#     数据集表 {
#         int id PK "训练会话ID"
#         int userId FK "用户ID"
#         date date "训练日期"
#         varchar Name "名称"
#         int isMark "是否标注"
#     }
#     动作分析表 {
#         int id PK "分析ID"
#         int datasetId FK "训练会话ID"
#         longtext result "关节坐标"
#     }
#
#     用户信息表 ||--o{ 数据集表 : "拥有"
#     数据集表 ||--o{ 动作分析表 : "对应"
