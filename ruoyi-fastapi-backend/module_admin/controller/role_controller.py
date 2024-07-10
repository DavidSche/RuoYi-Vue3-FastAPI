from fastapi import APIRouter, Request
from fastapi import Depends
from pydantic_validation_decorator import ValidateFields
from config.get_db import get_db
from module_admin.service.login_service import LoginService, CurrentUserModel
from module_admin.service.role_service import *
from module_admin.service.dept_service import DeptService, DeptModel
from module_admin.service.user_service import UserService, UserRoleQueryModel, UserRolePageQueryModel, CrudUserRoleModel
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.aspect.data_scope import GetDataScope
from module_admin.annotation.log_annotation import log_decorator
from config.enums import BusinessType
from utils.response_util import *
from utils.log_util import *
from utils.page_util import PageResponseModel
from utils.common_util import bytes2file_response


roleController = APIRouter(prefix='/system/role', dependencies=[Depends(LoginService.get_current_user)])


@roleController.get("/deptTree/{role_id}", dependencies=[Depends(CheckUserInterfaceAuth('system:role:query'))])
async def get_system_role_dept_tree(request: Request, role_id: int, query_db: AsyncSession = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysDept'))):
    dept_query_result = await DeptService.get_dept_tree_services(query_db, DeptModel(**{}), data_scope_sql)
    role_dept_query_result = await RoleService.get_role_dept_tree_services(query_db, role_id)
    role_dept_query_result.depts = dept_query_result
    logger.info('获取成功')

    return ResponseUtil.success(model_content=role_dept_query_result)
    
    
@roleController.get("/list", response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:role:list'))])
async def get_system_role_list(request: Request, role_page_query: RolePageQueryModel = Depends(RolePageQueryModel.as_query), query_db: AsyncSession = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('role_query.columns'))):
    role_page_query_result = await RoleService.get_role_list_services(query_db, role_page_query, data_scope_sql, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=role_page_query_result)
    
    
@roleController.post("", dependencies=[Depends(CheckUserInterfaceAuth('system:role:add'))])
@ValidateFields(validate_model='add_role')
@log_decorator(title='角色管理', business_type=BusinessType.INSERT)
async def add_system_role(request: Request, add_role: AddRoleModel, query_db: AsyncSession = Depends(get_db), current_user: CurrentUserModel = Depends(LoginService.get_current_user)):
    add_role.create_by = current_user.user.user_name
    add_role.create_time = datetime.now()
    add_role.update_by = current_user.user.user_name
    add_role.update_time = datetime.now()
    add_role_result = await RoleService.add_role_services(query_db, add_role)
    logger.info(add_role_result.message)

    return ResponseUtil.success(msg=add_role_result.message)
    
    
@roleController.put("", dependencies=[Depends(CheckUserInterfaceAuth('system:role:edit'))])
@ValidateFields(validate_model='edit_role')
@log_decorator(title='角色管理', business_type=BusinessType.UPDATE)
async def edit_system_role(request: Request, edit_role: AddRoleModel, query_db: AsyncSession = Depends(get_db), current_user: CurrentUserModel = Depends(LoginService.get_current_user), data_scope_sql: str = Depends(GetDataScope('role_query'))):
    await RoleService.check_role_allowed_services(edit_role)
    if not current_user.user.admin:
        await RoleService.check_role_data_scope_services(query_db, edit_role.role_id, data_scope_sql)
    edit_role.update_by = current_user.user.user_name
    edit_role.update_time = datetime.now()
    edit_role_result = await RoleService.edit_role_services(query_db, edit_role)
    logger.info(edit_role_result.message)

    return ResponseUtil.success(msg=edit_role_result.message)


@roleController.put("/dataScope", dependencies=[Depends(CheckUserInterfaceAuth('system:role:edit'))])
@log_decorator(title='角色管理', business_type=BusinessType.GRANT)
async def edit_system_role_datascope(request: Request, role_data_scope: AddRoleModel, query_db: AsyncSession = Depends(get_db), current_user: CurrentUserModel = Depends(LoginService.get_current_user), data_scope_sql: str = Depends(GetDataScope('role_query'))):
    await RoleService.check_role_allowed_services(role_data_scope)
    if not current_user.user.admin:
        await RoleService.check_role_data_scope_services(query_db, role_data_scope.role_id, data_scope_sql)
    edit_role = AddRoleModel(
        roleId=role_data_scope.role_id,
        dataScope=role_data_scope.data_scope,
        deptIds=role_data_scope.dept_ids,
        deptCheckStrictly=role_data_scope.dept_check_strictly,
        updateBy=current_user.user.user_name,
        updateTime=datetime.now()
    )
    role_data_scope_result = await RoleService.role_datascope_services(query_db, edit_role)
    logger.info(role_data_scope_result.message)

    return ResponseUtil.success(msg=role_data_scope_result.message)
    
    
@roleController.delete("/{role_ids}", dependencies=[Depends(CheckUserInterfaceAuth('system:role:remove'))])
@log_decorator(title='角色管理', business_type=BusinessType.DELETE)
async def delete_system_role(request: Request, role_ids: str, query_db: AsyncSession = Depends(get_db), current_user: CurrentUserModel = Depends(LoginService.get_current_user), data_scope_sql: str = Depends(GetDataScope('role_query'))):
    role_id_list = role_ids.split(',')
    for role_id in role_id_list:
        await RoleService.check_role_allowed_services(RoleModel(roleId=int(role_id)))
        if not current_user.user.admin:
            await RoleService.check_role_data_scope_services(query_db, int(role_id), data_scope_sql)
    delete_role = DeleteRoleModel(
        roleIds=role_ids,
        updateBy=current_user.user.user_name,
        updateTime=datetime.now()
    )
    delete_role_result = await RoleService.delete_role_services(query_db, delete_role)
    logger.info(delete_role_result.message)

    return ResponseUtil.success(msg=delete_role_result.message)
    
    
@roleController.get("/{role_id}", response_model=RoleModel, dependencies=[Depends(CheckUserInterfaceAuth('system:role:query'))])
async def query_detail_system_role(request: Request, role_id: int, query_db: AsyncSession = Depends(get_db), current_user: CurrentUserModel = Depends(LoginService.get_current_user), data_scope_sql: str = Depends(GetDataScope('role_query'))):
    if not current_user.user.admin:
        await RoleService.check_role_data_scope_services(query_db, role_id, data_scope_sql)
    role_detail_result = await RoleService.role_detail_services(query_db, role_id)
    logger.info(f'获取role_id为{role_id}的信息成功')

    return ResponseUtil.success(data=role_detail_result.model_dump(by_alias=True))


@roleController.post("/export", dependencies=[Depends(CheckUserInterfaceAuth('system:role:export'))])
@log_decorator(title='角色管理', business_type=BusinessType.EXPORT)
async def export_system_role_list(request: Request, role_page_query: RolePageQueryModel = Depends(RolePageQueryModel.as_form), query_db: AsyncSession = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('role_query'))):
    # 获取全量数据
    role_query_result = await RoleService.get_role_list_services(query_db, role_page_query, data_scope_sql, is_page=False)
    role_export_result = await RoleService.export_role_list_services(role_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(role_export_result))


@roleController.put("/changeStatus", dependencies=[Depends(CheckUserInterfaceAuth('system:role:edit'))])
@log_decorator(title='角色管理', business_type=BusinessType.UPDATE)
async def reset_system_role_status(request: Request, change_role: AddRoleModel, query_db: AsyncSession = Depends(get_db), current_user: CurrentUserModel = Depends(LoginService.get_current_user), data_scope_sql: str = Depends(GetDataScope('role_query'))):
    await RoleService.check_role_allowed_services(change_role)
    if not current_user.user.admin:
        await RoleService.check_role_data_scope_services(query_db, change_role.role_id, data_scope_sql)
    edit_role = AddRoleModel(
        roleId=change_role.role_id,
        status=change_role.status,
        updateBy=current_user.user.user_name,
        updateTime=datetime.now(),
        type='status'
    )
    edit_role_result = await RoleService.edit_role_services(query_db, edit_role)
    logger.info(edit_role_result.message)

    return ResponseUtil.success(msg=edit_role_result.message)


@roleController.get("/authUser/allocatedList", response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:role:list'))])
async def get_system_allocated_user_list(request: Request, user_role: UserRolePageQueryModel = Depends(UserRolePageQueryModel.as_query), query_db: AsyncSession = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysUser'))):
    role_user_allocated_page_query_result = await RoleService.get_role_user_allocated_list_services(query_db, user_role, data_scope_sql, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=role_user_allocated_page_query_result)


@roleController.get("/authUser/unallocatedList", response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:role:list'))])
async def get_system_unallocated_user_list(request: Request, user_role: UserRolePageQueryModel = Depends(UserRolePageQueryModel.as_query), query_db: AsyncSession = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysUser'))):
    role_user_unallocated_page_query_result = await RoleService.get_role_user_unallocated_list_services(query_db, user_role, data_scope_sql, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=role_user_unallocated_page_query_result)


@roleController.put("/authUser/selectAll", dependencies=[Depends(CheckUserInterfaceAuth('system:role:edit'))])
@log_decorator(title='角色管理', business_type=BusinessType.GRANT)
async def add_system_role_user(request: Request, add_role_user: CrudUserRoleModel = Depends(CrudUserRoleModel.as_query), query_db: AsyncSession = Depends(get_db), current_user: CurrentUserModel = Depends(LoginService.get_current_user), data_scope_sql: str = Depends(GetDataScope('role_query'))):
    if not current_user.user.admin:
        await RoleService.check_role_data_scope_services(query_db, add_role_user.role_id, data_scope_sql)
    add_role_user_result = await UserService.add_user_role_services(query_db, add_role_user)
    logger.info(add_role_user_result.message)

    return ResponseUtil.success(msg=add_role_user_result.message)


@roleController.put("/authUser/cancel", dependencies=[Depends(CheckUserInterfaceAuth('system:role:edit'))])
@log_decorator(title='角色管理', business_type=BusinessType.GRANT)
async def cancel_system_role_user(request: Request, cancel_user_role: CrudUserRoleModel, query_db: AsyncSession = Depends(get_db)):
    cancel_user_role_result = await UserService.delete_user_role_services(query_db, cancel_user_role)
    logger.info(cancel_user_role_result.message)

    return ResponseUtil.success(msg=cancel_user_role_result.message)


@roleController.put("/authUser/cancelAll", dependencies=[Depends(CheckUserInterfaceAuth('system:role:edit'))])
@log_decorator(title='角色管理', business_type=BusinessType.GRANT)
async def batch_cancel_system_role_user(request: Request, batch_cancel_user_role: CrudUserRoleModel = Depends(CrudUserRoleModel.as_query), query_db: AsyncSession = Depends(get_db)):
    batch_cancel_user_role_result = await UserService.delete_user_role_services(query_db, batch_cancel_user_role)
    logger.info(batch_cancel_user_role_result.message)

    return ResponseUtil.success(msg=batch_cancel_user_role_result.message)
