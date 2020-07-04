
<template>

  <div  >
    <mt-header fixed v-bind:title="headerTitle"></mt-header>
    <div style="margin-top: 50px;">

      <router-link :to="{path:  '/' +menu.menuHref }"  v-for="menu in menus" :key="menu">
        <mt-cell      v-bind:title="menu.menuName" value=""></mt-cell>
      </router-link>
    </div>
  </div>
</template>

<script>
    export default {
        name: "PersonalCenter",
        data(){
          return {
            headerTitle:"个人中心",
           menus:[{menuName:"登录",menuHref:"PersonalLogin"},
                   {menuName:"注册",menuHref:"PersonalCenterLogin"},
                   {menuName:"找回密码",menuHref:""}]
          }
        }
    }
</script>

<style scoped>

</style>
