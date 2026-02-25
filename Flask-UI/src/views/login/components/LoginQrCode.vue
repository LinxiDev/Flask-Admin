<script setup lang="ts">
import Motion from "../utils/motion";
import ReQrcode from "@/components/ReQrcode";
import { useUserStoreHook } from "@/store/modules/user";
import { buildUUID } from "@pureadmin/utils";
import { getWxLogin } from "@/api/user";
import { message } from "@/utils/message";
import { getTopMenu, initRouter } from "@/router/utils";
import { ref, onUnmounted } from "vue";
import router from "@/router";
import { setToken } from "@/utils/auth";

const state = buildUUID();
const disabled = ref(false);
const tips = ref("请使用微信扫码登录");
const tipsType = ref("warning"); // 'warning' 为黄色, 'success' 为绿色
const host = `${window.location.origin}/api/auth/wxLogin`;
const url = `https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxd0eef24ce7b830c6&redirect_uri=${encodeURIComponent(host)}&response_type=code&scope=snsapi_userinfo&state=${state}#wechat_redirect`;

const disabledClick = function () {
  tips.value = "请使用微信扫码登录";
  tipsType.value = "warning";
  disabled.value = true;
};

// 使用 ref 来存储定时器ID
const timer = ref();

const startTimer = () => {
  timer.value = setInterval(() => {
    getWxLogin({ state })
      .then(res => {
        if (res.success) {
          // 成功时立即清理定时器
          if (timer.value) {
            clearInterval(timer.value);
            timer.value = null;
          }
          disabled.value = true;
          tips.value = "登录成功";
          tipsType.value = "success"; // 设置为绿色
          setToken(res.data);
          // 获取后端路由
          initRouter()
            .then(() => {
              router
                .push(getTopMenu(true).path)
                .then(() => {
                  useUserStoreHook().SET_CURRENTPAGE(0);
                  message("登录成功", { type: "success" });
                })
                .catch(() => {
                  // 路由跳转失败时也要确保按钮状态正确
                  disabled.value = false;
                });
            })
            .catch(() => {
              // 路由初始化失败时的处理
              message("路由初始化失败", { type: "error" });
              disabled.value = false;
            });
        }
      })
      .catch(err => {
        // 请求失败时清理定时器
        if (timer.value) {
          clearInterval(timer.value);
          timer.value = null;
        }
        message(err.msg, { type: "error" });
      });
  }, 2000);
};

// 组件卸载时清理定时器
onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value);
    timer.value = null;
  }
});

// 启动定时器
startTimer();
</script>

<template>
  <Motion class="-mt-2 -mb-2">
    <div
      class="font-bold"
      :class="{
        'text-yellow-600': tipsType === 'warning',
        'text-green-600': tipsType === 'success'
      }"
    >
      {{ tips }}
    </div>
    <ReQrcode
      :text="url"
      :disabled="disabled"
      @disabled-click="disabledClick"
    />
  </Motion>
  <Motion :delay="100">
    <el-divider>
      <p class="text-gray-500 text-xs">扫码后点击"确认"，即可完成登录</p>
    </el-divider>
  </Motion>
  <Motion :delay="150">
    <el-button
      class="w-full mt-4!"
      @click="useUserStoreHook().SET_CURRENTPAGE(0)"
    >
      返回
    </el-button>
  </Motion>
</template>
