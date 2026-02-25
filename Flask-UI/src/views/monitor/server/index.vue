<template>
  <div class="monitor-server" v-loading="loading">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="border-none! shadow-sm mb-4">
          <template #header>
            <div class="flex items-center">
              <component :is="useRenderIcon(Cpu)" class="mr-2" />
              <span>CPU</span>
            </div>
          </template>
          <pure-table
            :data="cpuTable"
            :columns="cpuColumns"
            size="large"
            align-whole="center"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="border-none! shadow-sm mb-4">
          <template #header>
            <div class="flex items-center">
              <component :is="useRenderIcon(Memory)" class="mr-2" />
              <span>内存</span>
            </div>
          </template>
          <pure-table
            :data="memoryTable"
            :columns="memoryColumns"
            size="large"
            align-whole="center"
          />
        </el-card>
      </el-col>
    </el-row>

    <el-card class="border-none! shadow-sm mb-4">
      <template #header>
        <div class="flex items-center">
          <component :is="useRenderIcon(Monitor)" class="mr-2" />
          <span>服务器信息</span>
        </div>
      </template>
      <el-descriptions :column="4" border>
        <el-descriptions-item
          v-for="item in systemTable"
          :key="item.label"
          :label="item.label"
        >
          {{ item.value }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="border-none! shadow-sm mb-4">
      <template #header>
        <div class="flex items-center">
          <component :is="useRenderIcon(CoffeeCup)" class="mr-2" />
          <span>运行时信息</span>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item
          v-for="item in runtimeTable"
          :key="item.label"
          :label="item.label"
        >
          {{ item.value }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="border-none! shadow-sm">
      <template #header>
        <div class="flex items-center">
          <component :is="useRenderIcon(Disk)" class="mr-2" />
          <span>磁盘状态</span>
        </div>
      </template>
      <pure-table
        :data="server?.sysFiles"
        :columns="diskColumns"
        size="large"
        style="width: 100%"
        align-whole="center"
      >
        <template #usage="{ row }">
          <el-progress
            :text-inside="true"
            :stroke-width="26"
            :percentage="row.usage"
            :status="getUsageStatus(row.usage)"
            class="mb-4"
          />
        </template>
      </pure-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRole } from "./hook";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";

import Cpu from "~icons/ep/cpu";
import Memory from "~icons/ep/tickets";
import Monitor from "~icons/ep/monitor";
import CoffeeCup from "~icons/ep/coffee-cup";
import Disk from "~icons/ep/message-box";

defineOptions({
  name: "MonitorServer"
});

const {
  server,
  loading,
  cpuTable,
  memoryTable,
  systemTable,
  runtimeTable,
  cpuColumns,
  memoryColumns,
  diskColumns,
  getUsageStatus,
  getServerData
} = useRole();
</script>
