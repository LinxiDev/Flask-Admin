import { http } from "@/utils/http";

export interface Cpu {
  /** CPU核心数 */
  cpuNum: number;
  /** 用户使用率 (%) */
  used: number;
  /** 系统使用率 (%) */
  sys: number;
  /** 空闲率 (%) */
  free: number;
}

export interface Mem {
  /** 总内存 (GB) */
  total: number;
  /** 已用内存 (GB) */
  used: number;
  /** 剩余内存 (GB) */
  free: number;
  /** 使用率 (%) */
  usage: number;
}

export interface Runtime {
  /** 名称 */
  name: string;
  /** 版本 */
  version: string;
  /** 安装路径 */
  home: string;
  /** 启动时间（格式：yyyy-MM-dd HH:mm:ss） */
  startTime: string;
  /** 运行时长（如：12天3小时） */
  runTime: string;
  /** 启动参数 */
  inputArgs: string;
  /** 系统空闲内存 (MB) */
  free: number;
  /** 当前 Python 进程占用的内存总数 (MB) */
  total: number;
  /** 当前 Python 进程占用的内存 (MB) */
  used: number;
  /** Python 内存使用率 (%) */
  usage: number;
}

export interface Sys {
  /** 服务器名称 */
  computerName: string;
  /** 操作系统名称 */
  osName: string;
  /** 服务器IP */
  computerIp: string;
  /** 系统架构 */
  osArch: string;
  /** 项目运行目录 */
  userDir: string;
}

export interface SysFile {
  /** 盘符路径 */
  dirName: string;
  /** 文件系统类型 */
  sysTypeName: string;
  /** 盘符类型（如：本地磁盘） */
  typeName: string;
  /** 总大小（如：100.5 GB） */
  total: string;
  /** 可用大小 */
  free: string;
  /** 已用大小 */
  used: string;
  /** 使用率 (%) */
  usage: number;
}

export interface ServerMonitorData {
  /** CPU信息 */
  cpu: Cpu;
  /** 内存信息 */
  mem: Mem;
  /** JVM信息 */
  runtime: Runtime;
  /** 系统信息 */
  sys: Sys;
  /** 磁盘信息列表 */
  sysFiles: SysFile[];
}

export type ServerMonitorResult = {
  success: boolean;
  data: ServerMonitorData;
};

/**
 * 获取服务器监控信息
 */
export const getServer = () => {
  return http.request<ServerMonitorResult>("get", "/sys/monitor/server");
};
