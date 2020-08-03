<template>
  <div id="app" style="background-image: url(https://picsum.photos/1360/630)"> 
<div class="foot" >
    <p>Patent Miner ©2019-2020</p>
</div>
    <router-view/>
  </div>

</template>
<style scoped>
    .foot{
			bottom:0;
      width:100%;
      height:40px;
			background-color:#b6b6b6;
      text-align: center;
      font-family: "宋体";
      font-size: 12px;
      color: #000;  
      /* padding:25px 45px 30px; */
			margin:0 auto;
			border-top: 6px solid #eff1f1;   
      color: #666666;
            /* margin-top: 30px;
            line-height: 2em; */
      position: absolute;

		}
</style>

