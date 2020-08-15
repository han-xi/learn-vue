<template>
  <div> 
    <div class="register-wrapper"> 
      <div id="register">
        <p class="title">注册</p>
        <el-form
          :model="ruleForm2"
          status-icon
          :rules="rules2"
          ref="ruleForm2"
          label-width="0"
          class="demo-ruleForm"
        >
          <!-- 用户名 -->
          <el-form-item prop="mail">
            <el-input v-model="ruleForm2.mail" auto-complete="off" prefix-icon="el-icon-user-solid" placeholder="请输入邮箱地址"></el-input>
          </el-form-item>
          <!-- 提交注册 -->
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm2')" :loading="flag" style="width:100%;">注册</el-button>
            <p class="login" @click="gotoLogin">已有账号？立即登录</p>
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
  name:"PersonalCenterRegister", 
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
      ruleForm2: {
        mail:""
      },
      rules2: {
        mail: [{ validator: checkMa, trigger: 'change' }],
      },
  
    }
  }, 
  methods: {
    // <!--提交注册-->
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {     
          this.flag=true
            user.register(this.ruleForm2.mail).then(res=>{
              this.flag=false
              //注册成功
                swal("亲爱的用户"+this.ruleForm2.mail+",感谢您注册patent账号。\n为了更好的管理您的账号，方便使用系统全部功能，我们还需要您登陆邮箱"+this.ruleForm2.mail+"来激活您的账号。\n您的邮箱会收到一封来自"+res.data.send_mail+"激活邮件。如果长时间未收到，请检查垃圾邮件。\n注意：您如果不在"+res.data.send_time+"天之内激活账户，您的账号将删除。"
)
              }).catch(error=>{
              //用户已经存在
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
    // <!--进入登录页-->
    gotoLogin() {
      this.$router.push({
        path: "/PersonalCenterLogin"
      });
    },
    // <!--验证用户名格式-->
    checkMail(str){
         let re = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (re.test(str)) {
        return true;
      } else {
        return false;
      }
    },
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
