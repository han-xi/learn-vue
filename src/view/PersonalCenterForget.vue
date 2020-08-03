<template>
  <div> 
    <div class="register-wrapper"> 
      <div id="register">
        <p class="title">忘记密码</p>
        <el-form
          :model="forgetPassword"
          status-icon
          :rules="rules2"
          ref="forgetPassword"
          label-width="0"
          class="demo-ruleForm"
        >
          <!-- 用户名 -->
          <el-form-item prop="mail">
            <el-input v-model="forgetPassword.mail" prefix-icon="el-icon-user-solid" auto-complete="off" placeholder="请输入已注册邮箱地址"></el-input>
          </el-form-item>
          <!-- 提交注册 -->
          <el-form-item>
            <el-button type="primary" @click="submitForm('forgetPassword')" :loading="flag" style="width:100%;">提交</el-button>
            <!-- <p class="login" @click="gotoLogin">已有账号？立即登录</p> -->
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script> 
 import user from "@/api/user";
import swal from 'sweetalert';

export default {
  name:"PersonalCenterForget", 
  data() {
    //<!--验证邮箱是否正确-->
    let checkMa =(rule,value,callback)=>{
      if (value === '') {
        callback(new Error('请输入邮箱地址'))
      } else if (!this.checkMail(value)) {
        callback(new Error('邮箱不合法'))
      } else {
        callback()
      }
    }

    return { 
      flag:false,
      forgetPassword: {
        mail:""
      },
      rules2: {
        mail: [{ validator: checkMa, trigger: 'change' }],
      },
    }
  }, 
  methods: { 
    // <!--提交-->
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.flag=true
            user.forget(this.forgetPassword.mail).then(res=>{
              this.flag=false
            //注册成功
              swal("链接已发送请及时查收")
             
            }).catch(error=>{
              this.flag=false
            if(error.response){  
              swal(error.response.data.error)
            }   
            })
          
        } else {
          console.log("error submit!!");
          return false;
        }
      })
    },
    // <!--验证用户名格式-->
    checkMail(str){
         let re = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (re.test(str)) {
        return true;
      } else {
        return false;
      }
    }
  }
};
</script>
<style scoped>
.loading-wrapper {
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: #aedff8;
  display: flex;
  align-items: center;
  justify-content: center;
}
.register-wrapper img {
  position: absolute;
  z-index: 1;
}
.register-wrapper {
  /* position: fixed; */
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  padding-top: 5%;
  padding-bottom: 100%;
}
#register {
  max-width: 340px;
  opacity: 0.8;
  margin: 0px auto;
  background: #fff !important;
  padding: 20px 40px;
  border-radius: 10px;
  position: relative;
  z-index: 9;
}
.title {
  font-size: 26px;
  line-height: 50px;
  font-weight: bold;
  margin: 10px;
  text-align: center;
}
.el-form-item {
  text-align: center;
}
.login {
  margin-top: 10px;
  font-size: 14px;
  line-height: 22px;
  color: #1ab2ff;
  cursor: pointer;
  text-align: left;
  text-indent: 8px;
  width: 160px;
}
.login:hover {
  color: #2c2fd6;
}
.code >>> .el-form-item__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.code button {
  margin-left: 20px;
  width: 140px;
  text-align: center;
}
.el-button--primary:focus {
  background: #409EFF;
  border-color: #409EFF;
  color: #fff;
}
</style>
