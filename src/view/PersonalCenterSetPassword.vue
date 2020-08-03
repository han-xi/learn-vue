<template>
  <div> 
    <div class="pw-wrapper"> 
      <div id="pw">
        <p class="title">设置密码</p>
        <el-form
          :model="SetPassword"
          status-icon
          :rules="rules2"
          ref="SetPassword"
          label-width="0"
          class="demo-ruleForm"
        >
       
          <!-- 旧密码 -->
           
          <el-form-item prop="oldpass" v-if="this.$route.query.username!=none">
            <el-input type="password" v-model="SetPassword.oldpass" prefix-icon="el-icon-lock" auto-complete="off" placeholder="输入原密码"></el-input>
          </el-form-item>
        
          <!-- 新密码 -->
          <el-form-item prop="pass">
            <el-input type="password" v-model="SetPassword.pass" prefix-icon="el-icon-lock" auto-complete="off" placeholder="输入密码"></el-input>
          </el-form-item>
          <!-- 确认密码 -->
          <el-form-item prop="checkPass">
            <el-input type="password" v-model="SetPassword.checkPass" prefix-icon="el-icon-lock" auto-complete="off" placeholder="确认密码"></el-input>
          </el-form-item>
          <!-- 提交注册 -->
          <el-form-item>
            <div v-if="this.$route.query.username===none">
            <el-button type="primary" @click="submitForm1('SetPassword')" :loading="flag"  style="width:100%;">提交</el-button>
            <p class="login" @click="gotoLogin">已有账号？立即登录</p>
            </div>
             <div v-else>
            <el-button type="primary" @click="submitForm2('SetPassword')" :loading="flag" style="width:100%;">提交</el-button>
            </div>
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
  name:"PersonalCenterSetPassword", 
  data() {

// <!--验证密码-->
    let validatePassOld = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"))
      } else if(!this.checkPass(value)){
         callback(new Error('密码格式不正确，密码长度大于6位且数字字母混合'))
      }
      else {
        callback()
      }
    }
    // <!--验证密码-->
    let validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"))
      } else if(!this.checkPass(value)){
         callback(new Error('密码格式不正确，密码长度大于6位且数字字母混合'))
      }
      else {
        if (this.SetPassword.checkPass !== "") {
          this.$refs.SetPassword.validateField("checkPass");
        }
        callback()
      }
    }
    // <!--二次验证密码-->
    let validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.SetPassword.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      } 
    };
    return { 
       flag:false,
      SetPassword: {
        pass: "",
        checkPass: "",
        oldpass:"",
      
      },
      rules2: {
        pass: [{ validator: validatePass, trigger: 'change' }],
        checkPass: [{ validator: validatePass2, trigger: 'change' }],
        oldpass: [{ validator: validatePassOld, trigger: 'change' }],
      },
    }
  }, 
  methods: {
 
    // <!--提交注册和忘记密码界面的密码-->
    submitForm1(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
            this.flag=true
         user.changepassword(this.SetPassword.pass).then(res=>{
             this.flag=false
            //注册成功
              swal("提交成功")
              this.$router.push({
                path: "/PersonalCenterLogin"
              }); 
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
    
    // <!--提交修改密码界面的密码-->
    submitForm2(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
            this.flag=true
         user.setpassword(this.SetPassword.oldpass,this.SetPassword.pass).then(res=>{
             this.flag=false
            //注册成功
              swal("提交成功")
            //   this.$router.push({
            //     path: "/PersonalCenterLogin"
            //   }); 
              this.$router.go(-1);//返回上一层
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
        // <!--进入登录页-->
    gotoLogin() {
      this.$router.push({
        path: "/PersonalCenterLogin"
      });
    },
    // <!--验证密码格式-->
    checkPass(str){
      let re =/^(?=.*[(a-z)|(A-Z)])(?=.*\d)[^]{6,16}$/
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
.pw-wrapper img {
  position: absolute;
  z-index: 1;
}
.pw-wrapper {
  /* position: fixed; */
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  padding-top: 5%;
  padding-bottom: 100%;
}
#pw {
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
