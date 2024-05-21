from django.db import models

# Create your models here.

# 支行信息表
class Bank_Branch(models.Model):
    # 支行名称是主码且不能为空
    branch_name = models.CharField(max_length=30, primary_key=True, null=False)
    # 支行所在城市
    branch_city = models.CharField(max_length=30)
    # 支行电话
    branch_tel = models.CharField(max_length=11)
    # 支行负责人
    branch_manager = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.branch_name}" # 返回支行名称
    
# 银行部门（部门号，支行名称，部门名称，部门经理）
class Bank_Department(models.Model):
    # 部门号是主码且不能为空
    department_id = models.AutoField(primary_key=True, null=False)
    # 部门所属支行，存在外键关联，设置为级联删除
    branch = models.ForeignKey(Bank_Branch, on_delete=models.CASCADE, related_name='Bank_department')
    # 部门名称
    department_name = models.CharField(max_length=30, null=False)
    # 部门经理
    department_manager = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.branch.branch_name}-{self.department_name}"
    
# 员工（<u>工号</u>，员工照片，姓名，性别，手机号，部门号）
class Bank_Staff(models.Model):
    # 工号为主码且不能为空
    staff_id = models.AutoField(primary_key=True, null=False)
    # 员工照片
    staff_photo = models.ImageField(upload_to='photos/%Y%m%d/', default='photos/GGbond.jpg')
    # 姓名
    staff_name = models.CharField(max_length=20, null=False)
    # 性别
    staff_sex = models.CharField(max_length=10, null=False)
    # 手机号
    staff_tel = models.CharField(max_length=11, null=False)
    # 部门号，存在外键关联，设置为级联删除
    department = models.ForeignKey(Bank_Department, on_delete=models.CASCADE, related_name='DepartmentStaff')
    
    def __str__(self):
        return f"{self.staff_id}-{self.staff_name}"

# 支行负责人（<u>工号</u>，支行名称）
class Branch_Manager(Bank_Staff):
    # 支行负责人是员工的子类
    branch_name = models.ForeignKey(Bank_Branch, on_delete=models.CASCADE, related_name='BranchManager')
    
    def __str__(self):
        return f"{self.staff_id}-{self.staff_name}"
    
# 部门经理（<u>工号</u>，部门号）
class  Department_Manager(Bank_Staff):
    # 部门经理是员工的子类
    department_id = models.ForeignKey(Bank_Department, on_delete=models.CASCADE, related_name='DepartmentManager')
    
    def __str__(self):
        return f"{self.staff_id}-{self.staff_name}"
