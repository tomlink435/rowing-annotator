<!--suppress ALL -->
<template>
      <div class="login">
        <div class="loginPart">
          <h2>用户登录</h2>
          <!-- 登录主体，表单 -->
          <el-form  ref="loginFormRef" :model="loginForm" :rules="loginFormRules" label-width="0px" style="margin-top: 5px;">
            <!-- 用户名 -->
            <div>
              <el-form-item prop="username" class="inputElement">
                <el-input type="text" v-model="loginForm.username" placeholder="用户名" :prefix-icon="User"></el-input>
              </el-form-item>
            </div>


            <!-- 密码 -->
            <el-form-item prop="password" class="inputElement">
              <el-input type="password" v-model="loginForm.password" placeholder="密码" :prefix-icon="Lock"></el-input>
            </el-form-item>

            <!-- 按钮 -->
            <el-form-item>
              <el-button type="primary" @click="handleLogin" style="margin-left: 40%">登录</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
</template>

<script lang="ts" setup>
import {reactive, ref} from "vue"
import axios from "axios";
import { useRouter } from "vue-router"
import {ElLoading} from "element-plus";
import { User, Lock } from "@element-plus/icons-vue"
import { type FormInstance, FormRules } from "element-plus"
import {decode, encode} from "js-base64";
import jsCookie from "js-cookie"
import { usePermissStore } from '../store/permiss';

const permiss = usePermissStore();
const loginFormRef = ref<FormInstance | null>(null)
const router = useRouter()
//登录表单
const loginForm = reactive({
  username: "",
  password: "",
})

//登录校验规则
const loginFormRules: FormRules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 5, max: 16, message: "长度在 5 到 16 个字符", trigger: "blur" }
  ],
}

//登录逻辑
const handleLogin = ()=>{
  const loading = ElLoading.service({
    lock: true,
    text: '进入标注系统......',
    background: 'rgba(255,255,255, 1)',
  })
  //表单验证
  loginFormRef.value?.validate((valid: boolean) => {
    if (valid) {
      //发起登录请求
      axios.post("/api/sign/signIn/", {
        userName:loginForm.username,
        password:loginForm.password,
      }).then((res) => {
        res = JSON.parse(res)
        //权限信息

        //页面跳转
        if (res.role=='1'||res.role=='2'){
          const keys = permiss.defaultList[res.role == '1' ? 'admin' : 'user'];
          permiss.handleSet(keys);
          localStorage.setItem('ms_keys', JSON.stringify(keys));

          //存储用户信息
          localStorage.setItem("userId", res.id);
          localStorage.setItem("userName", res.username);
          localStorage.setItem("role", res.role);
          router.push("/")
        }

      })
    }else{
      return false
    }

})
  loading.close()
}
</script>

<style lang="scss" scoped>
.loginPart{
  position:absolute;
  /*定位方式绝对定位absolute*/
  top:50%;
  left:50%;
  /*顶和高同时设置50%实现的是同时水平垂直居中效果*/
  transform:translate(-50%,-50%);
  /*实现块元素百分比下居中*/
  width:450px;
  padding:50px;
  background: rgba(0,0,0,.5);
  /*背景颜色为黑色，透明度为0.8*/
  box-sizing:border-box;
  /*box-sizing设置盒子模型的解析模式为怪异盒模型，
  将border和padding划归到width范围内*/
  box-shadow: 0px 15px 25px rgba(0,0,0,.5);
  /*边框阴影  水平阴影0 垂直阴影15px 模糊25px 颜色黑色透明度0.5*/
  border-radius:15px;
  /*边框圆角，四个角均为15px*/
}
.loginPart h2{
  margin:0 0 30px;
  padding:0;
  color: #fff;
  text-align:center;
  /*文字居中*/
}
.inputElement{
  margin-left: 15%;
}
.login{
  background-image: url("../assets/img_1.png");
  width:100%;
  height:100%;
}
</style>
