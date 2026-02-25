import { http } from "@/utils/http";

type Result = {
  success: boolean;
  data?: Array<any>;
};

type ResultTable = {
  success: boolean;
  data?: {
    /** 列表数据 */
    list: Array<any>;
    /** 总条目数 */
    total?: number;
    /** 每页显示条目个数 */
    pageSize?: number;
    /** 当前页数 */
    currentPage?: number;
  };
};

/** 获取系统管理-用户管理列表 */
export const getUserList = (params?: object) => {
  return http.request<ResultTable>("get", "/sys/user/list", { params });
};

/** 新增系统管理-用户管理列表 */
export const addUser = (data?: object) => {
  return http.request<Result>("post", "/sys/user", { data });
};

/** 修改系统管理-用户管理列表 */
export const putUser = (data?: object) => {
  return http.request<Result>("put", "/sys/user", { data });
};

/** 删除系统管理-用户管理列表 */
export const delUser = (ids: number[] | string[]) => {
  return http.request<Result>("delete", `/sys/user/${ids.join(",")}`);
};

/** 系统管理-用户管理-分配角色 */
export const assignRole = (data?: object) => {
  return http.request<Result>("put", "/sys/user/assignRole", { data });
};

/** 系统管理-用户管理-重置密码 */
export const resetPassword = (data?: object) => {
  return http.request<Result>("put", "/sys/user/resetPassword", { data });
};

/** 系统管理-用户管理-上传头像 */
export const uploadAvatar = (data?: object) => {
  return http.request<Result>("put", "/sys/user/uploadAvatar", { data });
};

/** 系统管理-用户管理-获取所有角色列表 */
export const getAllRoleList = () => {
  return http.request<Result>("get", "/sys/role/listAll");
};

/** 系统管理-用户管理-根据userId，获取对应角色id列表（userId：用户id） */
export const getRoleIds = (params?: object) => {
  return http.request<Result>("get", "/sys/user/roleIds", { params });
};

/** 获取系统管理-角色管理列表 */
export const getRoleList = (params?: object) => {
  return http.request<ResultTable>("get", "/sys/role/list", { params });
};

/** 添加系统管理-角色管理列表 */
export const addRole = (data?: object) => {
  return http.request<Result>("post", "/sys/role", { data });
};

/** 修改系统管理-角色管理列表 */
export const putRole = (data?: object) => {
  return http.request<Result>("put", "/sys/role", { data });
};

/** 删除系统管理-角色管理列表 */
export const delRole = (ids: number[] | string[]) => {
  return http.request<Result>("delete", `/sys/role/${ids.join(",")}`);
};

/** 获取系统管理-菜单管理列表 */
export const getMenuList = (params?: object) => {
  return http.request<Result>("get", "/sys/menu", { params });
};

/** 添加系统管理-菜单管理列表 */
export const addMenu = (data?: object) => {
  return http.request<Result>("post", "/sys/menu", { data });
};

/** 删除系统管理-菜单管理列表 */
export const delMenu = (ids: number[] | string[]) => {
  return http.request<Result>("delete", `/sys/menu/${ids.join(",")}`);
};

/** 更新系统管理-菜单管理列表 */
export const putMenu = (data?: object) => {
  return http.request<Result>("put", "/sys/menu", { data });
};

/** 获取系统管理-部门管理列表 */
export const getDeptList = (params?: object) => {
  return http.request<Result>("get", "/sys/dept/list", { params });
};

/** 添加系统管理-部门管理列表 */
export const addDept = (data?: object) => {
  return http.request<Result>("post", "/sys/dept", { data });
};

/** 删除系统管理-部门管理列表 */
export const delDept = (ids: number[] | string[]) => {
  return http.request<Result>("delete", `/sys/dept/${ids.join(",")}`);
};

/** 更新系统管理-部门管理列表 */
export const putDept = (data?: object) => {
  return http.request<Result>("put", "/sys/dept", { data });
};

/** 获取系统监控-在线用户列表 */
export const getOnlineLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/online-logs", { data });
};

/** 获取系统监控-登录日志列表 */
export const getLoginLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/sys/logs/loginLogs", { data });
};

/** 获取系统监控-登录日志批量删除 */
export const delLoginLogs = (ids: number[] | string[]) => {
  return http.request<Result>("delete", `/sys/logs/loginLogs/${ids.join(",")}`);
};

/** 获取系统监控-操作日志清空 */
export const clearLoginLogs = () => {
  return http.request<Result>("delete", "/sys/logs/loginLogs/clear");
};

/** 获取系统监控-操作日志列表 */
export const getOperationLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/sys/logs/operateLogs", { data });
};

/** 获取系统监控-操作日志批量删除 */
export const delOperationLogs = (ids: number[] | string[]) => {
  return http.request<Result>(
    "delete",
    `/sys/logs/operateLogs/${ids.join(",")}`
  );
};

/** 获取系统监控-操作日志列表清空 */
export const clearOperationLogs = () => {
  return http.request<Result>("delete", "/sys/logs/operateLogs/clear");
};

/** 获取系统监控-系统日志列表 */
export const getSystemLogsList = (data?: object) => {
  return http.request<ResultTable>("post", "/sys/logs/systemLogs", { data });
};

/** 获取系统监控-系统日志-根据 id 查日志详情 */
export const getSystemLogsDetail = (id?: number | string) => {
  return http.request<Result>("get", `/sys/logs/systemLogs/${id}`);
};

/** 获取系统监控-系统日志-批量删除日志 */
export const delSystemLogs = (ids: number[] | string[]) => {
  return http.request<Result>(
    "delete",
    `/sys/logs/systemLogs/${ids.join(",")}`
  );
};

/** 获取系统监控-系统日志-清空日志 */
export const clearSystemLogs = () => {
  return http.request<Result>("delete", "/sys/logs/systemLogs/clear");
};

/** 获取角色管理-权限-菜单权限 */
export const getRoleMenu = () => {
  return http.request<Result>("get", "/sys/role/roleMenu");
};

/** 获取角色管理-权限-菜单权限-根据角色 id 查对应菜单 */
export const getRoleMenuIds = (params?: object) => {
  return http.request<Result>("get", "/sys/role/getRoleMenuIds", { params });
};

/** 获取角色管理-权限-菜单权限-保存角色菜单权限 */
export const assignMenu = (data?: object) => {
  return http.request<Result>("post", "/sys/role/assignMenu", { data });
};
