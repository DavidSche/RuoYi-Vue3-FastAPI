from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, BigInteger, event, func
from config.database import Base,BasePlus
from utils.sqlalchemy_events import listen_events, on


@listen_events
class SysUser(BasePlus):
    """
    用户信息表
    """

    __tablename__ = 'sys_user'

    user_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    dept_id = Column(BigInteger, comment='部门ID')
    user_name = Column(String(30, collation='utf8_general_ci'), nullable=False, comment='用户账号')
    nick_name = Column(String(30, collation='utf8_general_ci'), nullable=False, comment='用户昵称')
    user_type = Column(String(2, collation='utf8_general_ci'), default='00', comment='用户类型（00系统用户）')
    email = Column(String(50, collation='utf8_general_ci'), default='', comment='用户邮箱')
    phonenumber = Column(String(11, collation='utf8_general_ci'), default='', comment='手机号码')
    sex = Column(String(1, collation='utf8_general_ci'), default='0', comment='用户性别（0男 1女 2未知）')
    avatar = Column(String(100, collation='utf8_general_ci'), default='', comment='头像地址')
    password = Column(String(100, collation='utf8_general_ci'), default='', comment='密码')
    status = Column(String(1, collation='utf8_general_ci'), default='0', comment='帐号状态（0正常 1停用）')
    del_flag = Column(String(1, collation='utf8_general_ci'), default='0', comment='删除标志（0代表存在 2代表删除）')
    login_ip = Column(String(128, collation='utf8_general_ci'), default='', comment='最后登录IP')
    login_date = Column(DateTime, comment='最后登录时间')
    # create_by = Column(String(64, collation='utf8_general_ci'), default='', comment='创建者')
    # create_time = Column(DateTime, comment='创建时间', default=datetime.now())
    # update_by = Column(String(64, collation='utf8_general_ci'), default='', comment='更新者')
    # update_time = Column(DateTime, comment='更新时间', default=datetime.now())
    remark = Column(String(500, collation='utf8_general_ci'), comment='备注')


    def set_timestamp(target):
        if hasattr(target, 'create_time') and target.create_time is None:
            target.create_time = datetime.utcnow()
        if hasattr(target, 'update_time'):
            target.update_time = datetime.utcnow()

    # 在模型映射到数据库后，绑定事件
    # @event.listens_for(SysUser, 'before_insert')
    # async def before_insert_listener(mapper, connection, target):
    #     target.create_time = datetime.utcnow()
    #     target.update_time = datetime.utcnow()
    #     target.create_by = "default_user"  # Set the creator
    #     target.update_by = "default_user"  # Set the updater
    # @on("before_insert")
    # def lowercase_username(mapper, conn, self):
    #     self.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     self.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     self.create_by = "default_user"  # Set the creator
    #     self.update_by = "default_user"  # Set the updater


class SysUserRole(Base):
    """
    用户和角色关联表
    """

    __tablename__ = 'sys_user_role'

    user_id = Column(BigInteger, primary_key=True, nullable=False, comment='用户ID')
    role_id = Column(BigInteger, primary_key=True, nullable=False, comment='角色ID')


class SysUserPost(Base):
    """
    用户与岗位关联表
    """

    __tablename__ = 'sys_user_post'

    user_id = Column(BigInteger, primary_key=True, nullable=False, comment='用户ID')
    post_id = Column(BigInteger, primary_key=True, nullable=False, comment='岗位ID')
