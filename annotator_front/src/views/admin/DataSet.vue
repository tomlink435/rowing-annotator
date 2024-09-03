<script lang="ts" setup>
import {reactive, ref} from "vue";
import axios from "axios";
import {ElMessage, ElMessageBox, UploadProps, UploadUserFile} from "element-plus";
import { UploadFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

//首先在setup中定义
const router = useRouter()
let originUrl = ref(0)
const has_data = ref(false)
let dataset = ref([])
const dialogFormVisible = ref(false)
const AddDialogFormVisible = ref(false)
const AddId = ref(0)
const searchName = ref("")
const dataSetAddForm = ref({
  name:'',
  describe:'',
  url:''
})
const total=ref(0)
// searchData-向后端分页查询的对象，即当前页和每页总数
const searchData=reactive({
  current:1,
  limit:6
})
const init = ()=>{
  axios.get("api/requester/getDataSet").then((res)=>{
  
    console.log(res);
      if (res[0]!=null){
        has_data.value = true
        dataset.value = res.slice(0,searchData.limit)
        total.value = res.length
      }else{
        has_data.value = false
      }
  })
}
const fileList = ref<UploadUserFile[]>([])

const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
}

const handlePreview: UploadProps['onPreview'] = (file) => {
  console.log(file)
}

//文件数量改变
const handleChange = (file,fileLists) =>{
  let execute = true
  fileList.value.forEach((item,index)=>{
    if (item.name==file.name){
      ElMessage.info(`有相同名称的文件${item.name}，已过滤`)
      execute = false
      return
    }
  })
  if (execute){
    fileList.value = fileLists
  }

}
const handleSuccess = (res,fileLists) =>{
  console.log(res.data)
}
//添加数据集
const addDataset = ()=>{
  if (AddId.value!=0){
    if(Object.keys(fileList.value).length === 0){
      ElMessage.error("请上传图片或者视频")
    }else{
      var param = new FormData();
      param.append("id", AddId.value)
      fileList.value.forEach((item, index) => {
        param.append("file", item.raw);
      })
      axios.post("api/requester/upload/", param).then((res) => {
        init()
      });
      ElMessage.success("添加成功")
      AddDialogFormVisible.value = false
    }
  }else{
    if (dataSetAddForm.value.name.trim()==''){
      ElMessage.error("请输入合适的数据集名称")
    }else if (dataSetAddForm.value.describe.trim()==''){
      ElMessage.error("请输入合适的数据集描述")
    }else if (Object.keys(fileList.value).length === 0){
      ElMessage.error("请上传图片或者视频")
    }else {
      var param = new FormData();
      param.append("name", dataSetAddForm.value.name)
      param.append("description", dataSetAddForm.value.describe)
      fileList.value.forEach((item, index) => {
        param.append("file", item.raw);
      })
      axios.post("api/requester/upload/", param).then((res) => {
        init()
      });
      ElMessage.success("创建成功")
      dataSetAddForm.value.name = ''
      dataSetAddForm.value.describe = ''
      dialogFormVisible.value = false
    }
  }
  init()
}

const openAddForm = ()=>{
  AddId.value = 0
  dialogFormVisible.value = true
}

const SearchDataSet = () =>{
  axios.post("api/requester/searchName/",{
    name:searchName.value
  }).then((res)=>{
    dataset.value = res.slice(0,searchData.limit)
    total.value = res.length
    searchData.current=1
  })
}

const jump = (row) =>{
  router.push({
    path: '/View',
    query: {
      id: row.id
    }
  })
}
const jumpAdd = (row) =>{
  AddId.value = row.id
  AddDialogFormVisible.value = true
}

const deleteDataSet = (row) =>{
    ElMessageBox.confirm(
        '这个操作将会删除数据集'+row.name+', 是否继续?',
        '警告',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning',
        }
    )
        .then(() => {
          axios.post("api/requester/delDataSet/",{
            "id":row.id
          }).then(()=>{
            ElMessage({
              type: 'success',
              message: '删除成功',
            })
            init()
          })
        })
        .catch(() => {
          ElMessage({
            type: 'info',
            message: '取消删除',
          })
        })

}
const downloadResults=(row)=>{
  axios.post("api/requester/downloadResults/",{
            "id":row.id
          }).then((response)=>{
            console.log(response)
            // debugger
           originUrl.value = response.url;
            let lastIndex = originUrl.value.lastIndexOf("\\")
    if(originUrl.value.includes('/')){
     lastIndex = originUrl.value.lastIndexOf("/")}
    originUrl.value = originUrl.value.substring(lastIndex + 1)
    console.log('2',originUrl.value);
    const url = "http://localhost:8000/static/" + originUrl.value
            window.open(url)
            init()
            ElMessage({
              type: 'success',
              message: '下载成功',
            })
            
          })
}

const getData = (currentPage) =>{
  console.log(currentPage)
  axios.get("api/requester/getDataSet").then((res)=>{
    dataset.value = res.slice(searchData.limit*(currentPage-1),searchData.limit*currentPage)
    searchData.current=currentPage
  })
}

const formatMark = (row) =>{
  if (row.is_mark==0){
    return "自动标注完成"
  }else if (row.is_mark==1){
    return "已发布"
  }else if(row.is_mark==2){
    return "人工标注完成"
  }else {
    return "自动标注中"
  }
}

const changeMark = (row) =>{
  ElMessageBox.confirm(
      '这个操作将会发布数据集'+row.name+'的标注任务, 是否继续?',
      '警告',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        axios.post("api/requester/changeMark/",{
          "id":row.id
        }).then(()=>{
          ElMessage({
            type: 'success',
            message: '发布成功',
          })
          init()
        })
      })
      .catch(() => {
        ElMessage({
          type: 'info',
          message: '取消发布',
        })
      })
}

init()
</script>

<template>
<div v-if="has_data">
  <el-card>
    <div style="margin-bottom: 20px">
      <el-input type="text" v-model="searchName" placeholder="数据集名称" style="width: 200px;"></el-input>
      <el-button type="primary" @click="SearchDataSet" style="margin-left: 20px">搜索</el-button>
      <el-button type="primary" @click="openAddForm" style="float: right">创建数据集</el-button>
    </div>
    <el-table
      :data="dataset"
      :header-cell-style="{'text-align':'center'}"
      :cell-style="{'text-align':'center'}"
      border>
    <el-table-column
      prop="name"
      label="数据集名称"
      width="200">
    </el-table-column>
      <el-table-column
          prop="describe"
          label="数据集描述"
          width="300">
      </el-table-column>
      <el-table-column
          prop="quantity"
          label="数据数量"
          width="100">
      </el-table-column>
      <el-table-column
          prop="create_time"
          label="创建时间"
          width="160">
      </el-table-column>

      <el-table-column
          prop="is_mark"
          label="标注情况"
          width="180"
          :formatter="formatMark">
      </el-table-column>
      <el-table-column
          label="操作"
          width="auto">
        <template style="display: flex" v-slot="scope">
          <el-button  @click="jump(scope.row)" type="primary" round>查看</el-button>
          <el-button  @click="deleteDataSet(scope.row)" type="danger" round>删除</el-button>
          <!-- <el-button  @click="jumpAdd(scope.row)" type="primary" round>添加数据</el-button> -->
          <el-button  @click="downloadResults(scope.row)" type="primary" v-if="scope.row.is_mark==1" round>下载结果</el-button>
          <el-button  @click="changeMark(scope.row)" v-if="scope.row.is_mark==0" type="primary" round>发布</el-button>
          <!-- <el-button  @click="changeMark(scope.row)" v-if="scope.row.is_mark==1" type="primary" round>收集</el-button> -->
          <!-- <el-button  @click="changeMark(scope.row)" type="primary" round>收集</el-button> -->
          
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        :current-page="searchData.current"
        :page-size="searchData.limit"
        :total="total"
        :pager-count="6"
        style="text-align: center;margin-top: 20px;"
        layout="jumper, prev, pager, next, total"
        @current-change="getData" />
  </el-card>

</div>
  <div v-else>
    <el-empty>
      <el-button type="primary" @click="openAddForm">创建数据集</el-button>
    </el-empty>
  </div>

  <el-dialog v-model="AddDialogFormVisible" title="添加数据" width="30%" :close-on-click-modal = false>
      <el-upload
          class="upload-demo"
          action="api/requester/upload/"
          drag
          multiple
          accept="image/*, video/*"
          :auto-upload="false"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :on-change="handleChange"
          :on-success="handleSuccess"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽到此处或者 <em>点击上传</em>
        </div>
      </el-upload>

    <div slot="footer" class="dialog-footer">
      <el-button @click="AddDialogFormVisible = false">取 消</el-button>
      <el-button type="primary" @click="addDataset">确 定</el-button>
    </div>
  </el-dialog>

  <el-dialog v-model="dialogFormVisible" title="创建数据集" width="30%" :close-on-click-modal = false>
    <el-form :model="dataSetAddForm" label-position="left">
      <el-form-item label="数据集名称" label-width="100px">
        <el-input type="text" v-model="dataSetAddForm.name" placeholder="数据集名称"></el-input>
      </el-form-item>
      <el-form-item label="数据集描述" label-width="100px">
        <el-input type="text" v-model="dataSetAddForm.describe" placeholder="数据集描述"></el-input>
      </el-form-item>
      <el-upload
          class="upload-demo"
          action="api/requester/upload/"
          drag
          multiple
          accept="image/*, video/*"
          :auto-upload="false"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :on-change="handleChange"
          :on-success="handleSuccess"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽到此处或者 <em>点击上传</em>
        </div>
      </el-upload>
    </el-form>

    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogFormVisible = false">取 消</el-button>
      <el-button type="primary" @click="addDataset">确 定</el-button>
    </div>
  </el-dialog>

</template>

<style scoped>

</style>