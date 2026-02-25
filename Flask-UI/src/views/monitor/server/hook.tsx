import { ref, onMounted, computed } from "vue";
import { getServer, type ServerMonitorData } from "@/api/monitor/server";
import { message } from "@/utils/message";

export function useRole() {
  const server = ref<ServerMonitorData>();
  const loading = ref(false);

  const getServerData = async () => {
    loading.value = true;
    try {
      const { data } = await getServer();
      server.value = data;
    } catch ({ response }) {
      message(
        response.data.msg ? response.data.msg : "获取服务器监控数据失败",
        { type: "error" }
      );
    } finally {
      loading.value = false;
    }
  };

  // CPU 表格数据
  const cpuTable = computed(() => {
    if (!server.value?.cpu) return [];
    const { cpuNum, used, sys, free } = server.value.cpu;
    return [
      { label: "核心数", value: cpuNum },
      { label: "用户使用率", value: `${used}%` },
      { label: "系统使用率", value: `${sys}%` },
      { label: "当前空闲率", value: `${free}%` }
    ];
  });

  // CPU 表格列配置
  const cpuColumns = [
    { prop: "label", label: "属性" },
    { prop: "value", label: "值" }
  ];

  // 内存表格数据
  const memoryTable = computed(() => {
    if (!server.value?.mem || !server.value?.runtime) return [];
    const { total, used, free, usage } = server.value.mem;
    const rt = server.value.runtime as any;
    return [
      {
        label: "总内存",
        sysValue: `${total} GB`,
        runtimeValue: rt.total ? `${rt.total} MB` : "—"
      },
      {
        label: "已用内存",
        sysValue: `${used} GB`,
        runtimeValue: rt.used ? `${rt.used} MB` : "—"
      },
      {
        label: "剩余内存",
        sysValue: `${free} GB`,
        runtimeValue: rt.free ? `${rt.free} MB` : "—"
      },
      {
        label: "使用率",
        sysValue: `${usage}%`,
        runtimeValue: rt.usage ? `${rt.usage}%` : "—"
      }
    ];
  });

  // 内存表格列配置
  const memoryColumns = [
    { prop: "label", label: "属性" },
    { prop: "sysValue", label: "内存" },
    { prop: "runtimeValue", label: "Runtime" }
  ];

  // 系统信息表格数据
  const systemTable = computed(() => {
    if (!server.value?.sys) return [];
    const { computerName, osName, computerIp, osArch } = server.value.sys;
    return [
      { label: "服务器名称", value: computerName },
      { label: "操作系统", value: osName },
      { label: "服务器IP", value: computerIp },
      { label: "系统架构", value: osArch }
    ];
  });

  // 运行时信息表格数据
  const runtimeTable = computed(() => {
    if (!server.value?.runtime || !server.value?.sys) return [];
    const { name, version, startTime, runTime, home, inputArgs } =
      server.value.runtime;
    const { userDir } = server.value.sys;
    return [
      { label: "名称", value: name },
      { label: "版本", value: version },
      { label: "启动时间", value: startTime },
      { label: "运行时长", value: runTime },
      { label: "安装路径", value: home },
      { label: "项目路径", value: userDir },
      { label: "启动参数", value: inputArgs }
    ];
  });

  // 磁盘表格列配置
  const diskColumns = [
    { prop: "dirName", label: "盘符路径", minWidth: 120 },
    { prop: "sysTypeName", label: "文件系统", minWidth: 120 },
    { prop: "typeName", label: "盘符类型", minWidth: 120 },
    { prop: "total", label: "总大小", minWidth: 120 },
    { prop: "free", label: "可用大小", minWidth: 120 },
    { prop: "used", label: "已用大小", minWidth: 120 },
    {
      label: "已用百分比",
      minWidth: 150,
      slot: "usage"
    }
  ];

  const getUsageStatus = (usage: number) => {
    if (usage >= 90) {
      return "exception"; // ≥90%：严重，红色
    } else if (usage >= 75) {
      return "warning"; // 75%~89%：警告，橙色
    } else if (usage >= 50) {
      return "warning"; // 50%~74%：也可用 warning，或自定义为普通提醒
    } else {
      return "success"; // <50%：正常，绿色
    }
  };

  onMounted(() => {
    getServerData();
  });

  return {
    server,
    loading,
    getServerData,
    cpuTable,
    memoryTable,
    systemTable,
    runtimeTable,
    cpuColumns,
    memoryColumns,
    diskColumns,
    getUsageStatus
  };
}
