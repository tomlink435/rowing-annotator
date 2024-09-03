<script setup lang="ts">
import { useRoute } from 'vue-router'
import { DrawImg } from "@/assets/js/markTools";
import { getCurrentInstance, nextTick, onBeforeMount, onBeforeUpdate, onMounted, onUpdated, ref, render } from "vue";
import axios from "axios";
import { ElMessage } from "element-plus";
const route = useRoute()
const Url = ref("")
const imgDataList = ref(null)
const imgRef = ref()
//视频or图片
const videoSrc = ref(); // 视频文件路径
const videoPlayer = ref(null); // 视频播放器的DOM引用
let isPlaying = ref(false); // 视频播放状态

const currentFrame = ref(0);
const videoDuration = ref(0);
const currentIndex = ref(0)
const Frame = ref(0)
let originUrl = ref(0)

const FinalFrame = ref(0)
const pause = ref(false)
// 切换播放/暂停状态
const togglePlayPause = () => {
  if (isPlaying.value) {
    videoPlayer.value.pause();
  } else {
    videoPlayer.value.play();
  }
  isPlaying.value = !isPlaying.value;
};


const isVideo = ref(false)
const naHeight = ref(0)
const naWidth = ref(0)
const twoDArray = ref([[0, 1], [0, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 6], [5, 7],
[6, 8], [7, 9], [8, 10], [5, 11], [6, 12], [11, 12], [11, 13], [12, 14], [13, 15], [14, 16]])


function isVideoFile(fileName) {
  // 获取文件的扩展名
  const extension = fileName.split('.').pop().toLowerCase();

  // 定义常见的视频格式
  const videoExtensions = ['mp4', 'avi', 'mkv', 'flv', 'mov', 'wmv', 'rmvb', 'webm'];

  // 检查扩展名是否在视频格式列表中
  return videoExtensions.includes(extension);
}

const changeImg = (index) => {
  currentIndex.value = index
  originUrl.value = imgDataList.value[index].url
  let lastIndex = originUrl.value.lastIndexOf("\\")
  if(originUrl.value.includes('/')){
     lastIndex = originUrl.value.lastIndexOf("/")}
  originUrl.value = originUrl.value.substring(lastIndex + 1)
    if (isVideoFile(originUrl.value)) {
      axios.post("api/requester/getFrame/", {
        video: imgDataList.value[currentIndex.value].url
      }).then((res) => {
        Frame.value = res
        console.log(res)
      })
      isVideo.value = true
      videoSrc.value = "http://localhost:8000/static/" + originUrl.value

    } else {
      Url.value = "http://localhost:8000/static/" + originUrl.value
      isVideo.value = false
      console.log(Url.value)
    }

}

const getAllData = () => {
  axios.post("api/requester/getAllData/", {
    setId: route.query.id
  }).then((res) => {
    console.log(res)
    imgDataList.value = res
    originUrl.value = res[0].url
    console.log('1',originUrl.value);
    
    let lastIndex = originUrl.value.lastIndexOf("\\")
    if(originUrl.value.includes('/')){
     lastIndex = originUrl.value.lastIndexOf("/")}
    originUrl.value = originUrl.value.substring(lastIndex + 1)
    console.log('2',originUrl.value);

    if (isVideoFile(originUrl.value)) {
      isVideo.value = true
      videoSrc.value = "http://localhost:8000/static/" + originUrl.value
    } else {
      Url.value = "http://localhost:8000/static/" + originUrl.value
    }
    getDertSam()
  })
}
onMounted(() => {
  getAllData()
})


const getDertSam = () => {
  const ctx = document.querySelector("#canvas").getContext("2d");
  axios.post("api/requester/getFirstData/", {
    setId: route.query.id
  }).then((res) => {
    if (isVideoFile(res.url)) {
      axios.post("api/requester/getFrame/", {
        video: res.url
      }).then((res) => {
        Frame.value = res
        console.log(res)
      })
      handleVideoLoaded()
      let jsonPic1 = JSON.parse(res.result)
      //绘制帧数0时的点
      let jsonPic = jsonPic1[0]
      for (let j = 0; j < jsonPic.length; j++) {
        for (let i = 0; i < jsonPic[j].length; i++) {
          ctx.beginPath();
          ctx.arc(jsonPic[j][i][0] / (naWidth.value / videoPlayer.value.offsetWidth), jsonPic[j][i][1] /
            (naHeight.value / videoPlayer.value.offsetHeight), 2, 0, 2 * Math.PI);
          ctx.fillStyle = "#00ff00";
          ctx.fill();
          ctx.strokeStyle = "#00ff00";
          ctx.stroke();
        }
        let twoDArray1 = twoDArray.value;
        for (let k = 0; k < twoDArray1.length; k++) {
          let x1, y1, x2, y2;
          x1 = jsonPic[j][twoDArray1[k][0]][0] / (naWidth.value / videoPlayer.value.offsetWidth);
          y1 = jsonPic[j][twoDArray1[k][0]][1] / (naHeight.value / videoPlayer.value.offsetHeight);
          x2 = jsonPic[j][twoDArray1[k][1]][0] / (naWidth.value / videoPlayer.value.offsetWidth);
          y2 = jsonPic[j][twoDArray1[k][1]][1] / (naHeight.value / videoPlayer.value.offsetHeight);
          // console.log(videoPlayer.value.offsetWidth)
          // console.log(x1,y1,x2,y2)
          ctx.moveTo(x1, y1) //第一个点的坐标
          ctx.lineTo(x2, y2) //第二个点的坐标
          ctx.stroke();
          ctx.stroke();
        }
      }
    } else {
      onImageLoad()
      let jsonPic = JSON.parse(res.result)
      for (let j = 0; j < jsonPic.length; j++) {
        for (let i = 0; i < jsonPic[j].length; i++) {
          ctx.beginPath();
          ctx.arc(jsonPic[j][i][0] / (naWidth.value / imgRef.value.offsetWidth), jsonPic[j][i][1] /
            (naHeight.value / imgRef.value.offsetHeight), 2, 0, 2 * Math.PI);
          ctx.fillStyle = "#00ff00";
          ctx.fill();
          ctx.strokeStyle = "#00ff00";
          ctx.stroke();
        }
        let twoDArray1 = twoDArray.value;
        for (let k = 0; k < twoDArray1.length; k++) {
          let x1, y1, x2, y2;
          x1 = jsonPic[j][twoDArray1[k][0]][0] / (naWidth.value / imgRef.value.offsetWidth);
          y1 = jsonPic[j][twoDArray1[k][0]][1] / (naHeight.value / imgRef.value.offsetHeight);
          x2 = jsonPic[j][twoDArray1[k][1]][0] / (naWidth.value / imgRef.value.offsetWidth);
          y2 = jsonPic[j][twoDArray1[k][1]][1] / (naHeight.value / imgRef.value.offsetHeight);

          ctx.moveTo(x1, y1) //第一个点的坐标
          ctx.lineTo(x2, y2) //第二个点的坐标
          ctx.stroke();
          ctx.stroke();
        }
      }
    }
  })
}

const onImageLoad = () => {
  const imgElement = imgRef.value;
    let canvas = document.querySelector("#canvas");
    canvas.width = imgElement.offsetWidth;
    canvas.height = imgElement.offsetHeight;
    //原始图片大小
    naWidth.value = imgElement.naturalWidth;
    naHeight.value = imgElement.naturalHeight;

    if (isVideoFile(originUrl.value)) {
      axios.post("api/requester/getFrame/", {
        video: imgDataList.value[currentIndex.value].url
      }).then((res) => {
        Frame.value = res
        console.log(res)
      })
      isVideo.value = true
      videoSrc.value = "http://localhost:8000/static/" + originUrl.value

    } else {
      isVideo.value = false
      Url.value = "http://localhost:8000/static/" + originUrl.value

      console.log(Url.value);
      // debugger
      const c = document.querySelector('#canvas');

      const ctx = c.getContext("2d");
      let jsonPic = JSON.parse(imgDataList.value[currentIndex.value].result)

      for (let j = 0; j < jsonPic.length; j++) {
        for (let i = 0; i < jsonPic[j].length; i++) {
          ctx.beginPath();
          ctx.arc(jsonPic[j][i][0] / (naWidth.value / imgRef.value.offsetWidth), jsonPic[j][i][1] /
            (naHeight.value / imgRef.value.offsetHeight), 2, 0, 2 * Math.PI);
          ctx.fillStyle = "#00ff00";
          ctx.fill();
          ctx.strokeStyle = "#00ff00";
          ctx.stroke();
        }
        let twoDArray1 = twoDArray.value;
        for (let k = 0; k < twoDArray1.length; k++) {
          ctx.beginPath();
          let x1, y1, x2, y2;
          x1 = jsonPic[j][twoDArray1[k][0]][0] / (naWidth.value / imgRef.value.offsetWidth);
          y1 = jsonPic[j][twoDArray1[k][0]][1] / (naHeight.value / imgRef.value.offsetHeight);
          x2 = jsonPic[j][twoDArray1[k][1]][0] / (naWidth.value / imgRef.value.offsetWidth);
          y2 = jsonPic[j][twoDArray1[k][1]][1] / (naHeight.value / imgRef.value.offsetHeight);
          console.log(imgRef.value.offsetHeight)
          ctx.moveTo(x1, y1) //第一个点的坐标
          ctx.lineTo(x2, y2) //第二个点的坐标
          ctx.stroke();
        }
      }
    }
}
const handleVideoLoaded = () => {
  // 视频元数据已加载完成后，可以获取视频帧的尺寸
  const video = videoPlayer.value;
  if (video) {
    let canvas = document.querySelector("#canvas");
    canvas.width = video.offsetWidth;
    canvas.height = video.offsetHeight;
    //原始视频帧大小
    naWidth.value = video.videoWidth;
    naHeight.value = video.videoHeight;
    videoDuration.value = video.duration;
    // const videoTrack = video.getVideoTracks()[0]
    // const capabilities = videoTrack.getCapabilities();
    // console.log(capabilities.frameRate)
  }

};

const goToFrame = (frame) => {
  const video = videoPlayer.value;
  if (video) {
    // 将帧数转换为对应的时间（秒）并跳转到该时间点
    const time = frame / Frame.value;
    videoPlayer.value.currentTime = time;
    currentFrame.value = frame;
  }
};
const prevFrame = () => {
  const canvas = document.querySelector("#canvas")
  var w = canvas.width
  var h = canvas.height
  canvas.width = w
  canvas.height = h
  const ctx = canvas.getContext("2d");
  let jsonPic1 = JSON.parse(imgDataList.value[currentIndex.value].result)
  if (currentFrame.value > 1) {
    currentFrame.value -= 1;
    goToFrame(currentFrame.value);

    let jsonPic = jsonPic1[currentFrame.value - 1]
    for (let j = 0; j < jsonPic.length; j++) {
      for (let i = 0; i < jsonPic[j].length; i++) {
        ctx.beginPath();
        ctx.arc(jsonPic[j][i][0] / (naWidth.value / videoPlayer.value.offsetWidth), jsonPic[j][i][1] /
          (naHeight.value / videoPlayer.value.offsetHeight), 2, 0, 2 * Math.PI);
        ctx.fillStyle = "#00ff00";
        ctx.fill();
        ctx.strokeStyle = "#00ff00";
        ctx.stroke();
      }
      let twoDArray1 = twoDArray.value;
      for (let k = 0; k < twoDArray1.length; k++) {
        let x1, y1, x2, y2;
        x1 = jsonPic[j][twoDArray1[k][0]][0] / (naWidth.value / videoPlayer.value.offsetWidth);
        y1 = jsonPic[j][twoDArray1[k][0]][1] / (naHeight.value / videoPlayer.value.offsetHeight);
        x2 = jsonPic[j][twoDArray1[k][1]][0] / (naWidth.value / videoPlayer.value.offsetWidth);
        y2 = jsonPic[j][twoDArray1[k][1]][1] / (naHeight.value / videoPlayer.value.offsetHeight);
        // console.log(videoPlayer.value.offsetWidth)
        // console.log(x1,y1,x2,y2)
        ctx.moveTo(x1, y1) //第一个点的坐标
        ctx.lineTo(x2, y2) //第二个点的坐标
        ctx.stroke();
        ctx.stroke();
      }
    }
  } else {
    ElMessage.info("已经是第一帧")
  }

};

const nextFrame = () => {
  const canvas = document.querySelector("#canvas")
  var w = canvas.width
  var h = canvas.height
  canvas.width = w
  canvas.height = h
  const ctx = canvas.getContext("2d");
  let jsonPic1 = JSON.parse(imgDataList.value[currentIndex.value].result)
  if (currentFrame.value < videoDuration.value * Frame.value && currentFrame.value < jsonPic1.length) {
    currentFrame.value += 1;
    goToFrame(currentFrame.value);
    let jsonPic = jsonPic1[currentFrame.value - 1]
    for (let j = 0; j < jsonPic.length; j++) {
      for (let i = 0; i < jsonPic[j].length; i++) {
        ctx.beginPath();
        ctx.arc(jsonPic[j][i][0] / (naWidth.value / videoPlayer.value.offsetWidth), jsonPic[j][i][1] /
          (naHeight.value / videoPlayer.value.offsetHeight), 2, 0, 2 * Math.PI);
        ctx.fillStyle = "#00ff00";
        ctx.fill();
        ctx.strokeStyle = "#00ff00";
        ctx.stroke();
      }
      let twoDArray1 = twoDArray.value;
      for (let k = 0; k < twoDArray1.length; k++) {
        let x1, y1, x2, y2;
        x1 = jsonPic[j][twoDArray1[k][0]][0] / (naWidth.value / videoPlayer.value.offsetWidth);
        y1 = jsonPic[j][twoDArray1[k][0]][1] / (naHeight.value / videoPlayer.value.offsetHeight);
        x2 = jsonPic[j][twoDArray1[k][1]][0] / (naWidth.value / videoPlayer.value.offsetWidth);
        y2 = jsonPic[j][twoDArray1[k][1]][1] / (naHeight.value / videoPlayer.value.offsetHeight);
        // console.log(videoPlayer.value.offsetWidth)
        // console.log(x1,y1,x2,y2)
        ctx.moveTo(x1, y1) //第一个点的坐标
        ctx.lineTo(x2, y2) //第二个点的坐标
        ctx.stroke();
        ctx.stroke();
      }
    }
  } else {
    ElMessage.info("已经到最后一帧")
  }

  /* let  index = currentFrame.value*Frame.value/25*/



};
// 视频播放结束事件处理
const onVideoEnded = () => {
  isPlaying.value = false;
  FinalFrame.value = currentFrame.value
  console.log("end")
  // 在这里可以添加视频结束后的逻辑，比如播放下一个视频等。
};
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function forLoopWithDelay(start, end, interval) {
  for (let i = start; i < end; i++) {
    if (pause.value){
      break
    }
    nextFrame()
    await delay(interval);
  }
}

const PlayFrame = () =>{
  isPlaying.value = true
  pause.value = false
  if (currentFrame.value==FinalFrame.value){
    currentFrame.value=0
  }
  const video = videoPlayer.value
  video.play()
  let jsonPic1 = JSON.parse(imgDataList.value[currentIndex.value].result)
  console.log("play")
// 使用示例
  forLoopWithDelay(currentFrame.value, jsonPic1.length, 1000/Frame.value).then(() =>
      console.log("调用完成"));
}


const StopFrame = () =>{
  const video = videoPlayer.value
  pause.value = true
  isPlaying.value = false
  video.pause()
}
</script>

<template>
  <div style="margin: 0 2px">

    <!-- 工作视图区 -->
    <div class="row view">
      <p v-if="isVideo">当前帧数: {{ currentFrame }}</p>
      <div class="col-md-9" v-if="isVideo" style="display: flex">

        <canvas ref="canvas" id="canvas" style="border: 1px black solid; position:absolute;z-index: 3">

        </canvas>
        <video ref="videoPlayer" :src="videoSrc" @loadeddata="handleVideoLoaded" @ended="onVideoEnded" id="video" controls
          style="width:70%;height:auto;z-index: 2"></video>


      </div>
      <!-- 主视图，显示图片 -->
      <div class="col-md-9" v-else>
        <canvas ref="canvas" id="canvas" style="border: 1px black solid; position:absolute;z-index: 3"> </canvas>

        <img ref="imgRef" id="img" class="img" @load="onImageLoad" :src=Url alt=""
          style="width:70%;height:auto;z-index: 1" />
      </div>
      <!-- 画布底部留白 -->
      <div style="width:100%;height:70px;"></div>
    </div>

    <!-- 侧边工具栏 -->
    <div :class="{ 'col-md-3': true, viewtoolsflex: false, viewtools: true }">
      <div class="tools">
      </div>

      <!-- 图片列表 -->
      <div style="margin-top: 10px;">
        <!-- 滚动框 -->
        <div>
          <div v-if="isVideo">
            <el-button @click="prevFrame" type="primary">上一帧</el-button>
            <el-button @click="nextFrame" type="primary">下一帧</el-button>
            <el-button @click="PlayFrame" type="primary">播放</el-button>
            <el-button @click="StopFrame" type="primary">暂停</el-button>
          </div>


          <div style="width: 100%; margin: 0 auto; " class="row">
            <!-- 图片列表主体 -->
            <span v-for="(item, index) in imgDataList" :key="item.id" class="col-md-3">
              <el-button :id="item.id" size="default" style="margin:10px" @click="changeImg(index)">
                {{ index + 1 }}
              </el-button>
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.viewpic {
  width: 700px;
  height: 500px;
  padding: 0px;
  background-color: rgba(179, 179, 179, 0.39);
  text-align: center;
  position: relative;
  /* .img{
     width: 700px;
     height: 500px;
  } */
}

.information {
  position: absolute;
  z-index: 6;
}

.box-card {
  background-color: rgba(0, 200, 255, 0);
  border: 0px;
  text-align: left;
}

.toolbox {
  background-color: rgb(56, 203, 247);
  height: 35px;
  font-size: 20px;
  border-radius: 5px;
  text-align: center;
}

.tools {
  text-align: left;
  margin-top: 5px;
}

.previewdiv {
  margin-top: 5px;
  background-color: rgb(211, 210, 210);
}

.location {
  margin-top: 5px;
}

.location>div {
  margin-top: 1px;
}

.viewtoolsflex {
  position: fixed;
  top: 0px;
  /* left: 1510px; */
  left: 79.15%;
  padding: 0px;
  /* width: 390px; */
  width: 20.25%;
}

.viewtools {
  position: absolute;
  top: 34.5px;
  /* left: 1203px */
  left: 74.5%;
  padding: 0px;
  /* width: 390px; */
  width: 24%;
}

.suspensionButtonArea {
  /* background-color: aqua; */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;

  position: fixed;
  bottom: 10px;
  /*可以通过改变top的百分比，来改变上下的位置*/
  left: 45%;
  /*可以通过改变left的百分比，来改变左右的位置*/
}
</style>