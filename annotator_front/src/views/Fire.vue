<script lang="ts" setup>
import {ref} from 'vue';
import axios from "axios";

// 初始化数据和Canvas设置：
// 使用axios从一个API接口获取数据，存储于dataList中。
// 初始化一个二维数组twoDArray，用于定义火柴人身体各部分之间的连接。
// 使用多个ref来管理复选框的状态，以决定哪些部分应该在动画中显示。
// 动画渲染逻辑：
// start函数用于绘制每一帧的火柴人。它首先清除Canvas，然后根据dataList中的坐标绘制点和线。
// 通过twoDArray定义的连接关系，使用Canvas的路径绘制API来绘制火柴人的身体部分。
// 提供了一个forLoopWithDelay函数，通过异步延迟来连续播放动画帧。
// 交互功能：
// 通过复选框允许用户选择要显示的身体部分。每个复选框的改变会更新checkList2数组，这影响了动画的渲染。
// PlayFrame函数用于启动动画，通过循环调用start函数实现连续播放。
// 模板和样式：
// 在Vue模板中定义了Canvas和一组复选框，用于控制动画的播放和显示的身体部分。
// 使用Element UI组件库来提升界面的交互性和视觉效果。

const dataList = ref(null)
const twoDArray = ref([[0,1],[1,2],[1,3],[1,8],[1,9],[2,4],[4,6],[3,5],[5,7],[8,10],[10,12],[9,11],[11,13]])
const index = ref(6000)

const checked1 = ref(true)
const checked2 = ref(false)
const checked3 = ref(false)
const checked4 = ref(false)
const checked5 = ref(false)
const checked6 = ref(false)
const checked7 = ref(false)
const checked8 = ref(false)
const checked9 = ref(false)
const checked10 = ref(false)
const checked11 = ref(false)
const checked12 = ref(false)
const checked13 = ref(false)
const checked14 = ref(false)

const checkList = ref([])
const checkList2 = ref([])
const init = () =>{
  axios.post("/api/requester/test/").then((res)=>{
    dataList.value = res
    console.log(res)
  })
}

init()

const start = () =>{
  const canvas = document.querySelector("#canvas")
  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  let jsonPic = JSON.parse(dataList.value)
  for (let i = 0; i < jsonPic[index.value].length/2; i++) {
    let x = jsonPic[index.value][i*2];
    let y = jsonPic[index.value][i*2+1];

    // 设置画笔颜色和样式
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';  // 半透明的蓝色
    ctx.strokeStyle = 'rgba(0, 0, 0, 1)';  // 不透明度为1的蓝色描边
    ctx.lineWidth = 0.3;  // 设置线条宽度

    ctx.beginPath();
    ctx.arc( canvas.width - (x/10+200), canvas.height - y/10, 3, 0, Math.PI * 2);  // 使用半径为5的圆形画点，中心在(canvasWidth/2, canvasHeight/2)的位置
    ctx.fill();  // 用设置的填充颜色填充点
    ctx.stroke();  // 用设置的描边颜色描边点
  }

  if (index.value>41){
    for(let j = 40;j>0;j--){

      for (let i = 0; i < jsonPic[index.value-j].length/2; i++){

        if (checkList2.value.includes(i)){
          let x = jsonPic[index.value-j][i*2];
          let y = jsonPic[index.value-j][i*2+1];
          // 设置画笔颜色和样式
          ctx.fillStyle = 'rgba(10,500,0, 0.5)';  // 半透明的蓝色
          ctx.strokeStyle = 'rgba(0,0,0,1)';  // 不透明度为1的蓝色描边
          ctx.lineWidth = 0.3;  // 设置线条宽度

          ctx.beginPath();
          ctx.arc( canvas.width - (x/10+200), canvas.height - y/10, 0.1, 0, Math.PI * 2);  // 使用半径为5的圆形画点，中心在(canvasWidth/2, canvasHeight/2)的位置
          ctx.fill();  // 用设置的填充颜色填充点
          ctx.stroke();  // 用设置的描边颜色描边点
        }
      }

      // for(let k = 20;k>0;k--){
      //   for (let i = 0; i < jsonPic[index.value-j-k].length/2; i++){
      //     let x1, y1, x2, y2;
      //     x1 = canvas.width - (jsonPic[index.value-j-k][i*2]/10+200);
      //     y1 = canvas.height - (jsonPic[index.value-j-k][i*2+1]/10);
      //     x2 = canvas.width - (jsonPic[index.value-j-k-1][i*2]/10+200);
      //     y2 = canvas.height - (jsonPic[index.value-j-k-1][i*2+1]/10);
      //     ctx.moveTo(x1, y1) //第一个点的坐标
      //     ctx.lineTo(x2, y2) //第二个点的坐标
      //     ctx.stroke();
      //   }
      // }

    }
  }


  let twoDArray1 = twoDArray.value;
  for (let k = 0; k < twoDArray1.length; k++) {
    let x1, y1, x2, y2;
    x1 = canvas.width - (jsonPic[index.value][twoDArray1[k][0]*2] / 10 + 200);
    y1 = canvas.height - (jsonPic[index.value][twoDArray1[k][0]*2+1] / 10);
    x2 = canvas.width - (jsonPic[index.value][twoDArray1[k][1]*2] / 10 + 200);
    y2 = canvas.height - (jsonPic[index.value][twoDArray1[k][1]*2+1] / 10);
    // console.log(videoPlayer.value.offsetWidth)
    // console.log(x1,y1,x2,y2)
    ctx.moveTo(x1, y1) //第一个点的坐标
    ctx.lineTo(x2, y2) //第二个点的坐标
    ctx.stroke();
    ctx.stroke();
  }
  index.value = index.value+1
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function forLoopWithDelay(startTime, end, interval) {
  for (let i = startTime; i < end; i++) {
    start()
    await delay(interval);
  }
}

const PlayFrame = () =>{
  forLoopWithDelay(6000, 600000, 30).then(() =>
      console.log("调用完成"));

}
const changeCheckBox = () =>{
  if (checkList2.value.includes(0)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 0;
    });
  }else{
    checkList2.value.push(0)
  }
}
const changeCheckBox1 = () =>{
  if (checkList2.value.includes(1)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 1;
    });
  }else{
    checkList2.value.push(1)
  }
}

const changeCheckBox2 = () =>{
  if (checkList2.value.includes(2)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 2;
    });
  }else{
    checkList2.value.push(2)
  }
}

const changeCheckBox3 = () =>{
  if (checkList2.value.includes(3)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 3;
    });
  }else{
    checkList2.value.push(3)
  }
}

const changeCheckBox4 = () =>{
  if (checkList2.value.includes(4)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 4;
    });
  }else{
    checkList2.value.push(4)
  }
}

const changeCheckBox5 = () =>{
  if (checkList2.value.includes(5)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 5;
    });
  }else{
    checkList2.value.push(5)
  }
}

const changeCheckBox6 = () =>{
  if (checkList2.value.includes(6)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 6;
    });
  }else{
    checkList2.value.push(6)
  }
}

const changeCheckBox7 = () =>{
  if (checkList2.value.includes(7)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 7;
    });
  }else{
    checkList2.value.push(7)
  }
}

const changeCheckBox8= () =>{
  if (checkList2.value.includes(8)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 8;
    });
  }else{
    checkList2.value.push(8)
  }
}

const changeCheckBox9= () =>{
  if (checkList2.value.includes(9)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 9;
    });
  }else{
    checkList2.value.push(9)
  }
}

const changeCheckBox10= () =>{
  if (checkList2.value.includes(10)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 10;
    });
  }else{
    checkList2.value.push(10)
  }
}

const changeCheckBox11= () =>{
  if (checkList2.value.includes(11)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 11;
    });
  }else{
    checkList2.value.push(11)
  }
}

const changeCheckBox12= () =>{
  if (checkList2.value.includes(12)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 12;
    });
  }else{
    checkList2.value.push(12)
  }
}

const changeCheckBox13= () =>{
  if (checkList2.value.includes(13)){
    checkList2.value = checkList2.value.filter(function(item){
      return item !== 13;
    });
  }else{
    checkList2.value.push(13)
  }
}

</script>

<template>
  <div>
    <div>
      <canvas ref="canvas" id="canvas" style="border: 1px black solid; position:absolute; width: 1000px;height: 600px">
      </canvas>
      <el-button @click="PlayFrame" type="primary" style="float: right">火柴人启动</el-button>
      <el-checkbox-group v-model="checkList"  style="float: right;margin-top: 50px;width: 200px">
        <el-checkbox label="头部" size="large" @change="changeCheckBox" />
        <el-checkbox label="胸" size="large" @change="changeCheckBox1"/>
        <el-checkbox label="左肩" size="large" @change="changeCheckBox2"/>
        <el-checkbox label="右肩" size="large" @change="changeCheckBox3"/>
        <el-checkbox label="左手臂" size="large" @change="changeCheckBox4"/>
        <el-checkbox label="右手臂" size="large" @change="changeCheckBox5"/>
        <el-checkbox label="左手" size="large" @change="changeCheckBox6"/>
        <el-checkbox label="右手" size="large" @change="changeCheckBox7"/>
        <el-checkbox label="左大腿" size="large" @change="changeCheckBox8"/>
        <el-checkbox label="右大腿" size="large" @change="changeCheckBox9"/>
        <el-checkbox label="左胫骨" size="large" @change="changeCheckBox10"/>
        <el-checkbox label="右胫骨" size="large" @change="changeCheckBox11"/>
        <el-checkbox label="左脚" size="large" @change="changeCheckBox12"/>
        <el-checkbox label="右脚" size="large" @change="changeCheckBox13"/>
      </el-checkbox-group>

    </div>

  </div>


</template>

<style scoped>

</style>