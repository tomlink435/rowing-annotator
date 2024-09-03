<script lang="ts" setup>
import {reactive, ref} from "vue";
import axios from "axios";
import {ElMessage, ElMessageBox, UploadProps, UploadUserFile} from "element-plus";
import { useRouter } from 'vue-router'

//首先在setup中定义
const router = useRouter()
let dataset = ref([])
const dialogFormVisible = ref(false)
const searchName = ref("")

const total=ref(0)
// searchData-向后端分页查询的对象，即当前页和每页总数
const searchData=reactive({
  current:1,
  limit:6
})
const dataSetAddForm = reactive({
  username:'',
  password:''
})
const init = ()=>{
  axios.get("api/sign/getUser/").then((res)=>{
      dataset.value = res.slice(0,searchData.limit)
      total.value = res.length
  })
}

const SearchDataSet = () =>{
  axios.post("api/sign/searchUser/",{
    name:searchName.value
  }).then((res)=>{
    dataset.value = res.slice(0,searchData.limit)
    total.value = res.length
    searchData.current=1
  })
}

const jump = (row) =>{
  ElMessageBox.confirm(
      '这个操作将会重置账号'+row.name+'的密码为6个1, 是否继续?',
      '警告',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        axios.post("api/sign/changeUser/",{
          "id":row.id
        }).then(()=>{
          ElMessage({
            type: 'success',
            message: '重置成功',
          })
          init()
        })
      })
      .catch(() => {
        ElMessage({
          type: 'info',
          message: '取消重置',
        })
      })
}

const openAddForm = ()=>{
  dialogFormVisible.value = true
}

const getData = (currentPage) =>{
  console.log(currentPage)
  axios.get("api/sign/addUser/").then((res)=>{
    dataset.value = res.slice(searchData.limit*(currentPage-1),searchData.limit*currentPage)
    searchData.current=currentPage
  })
}
const addUser = () =>{
  if (dataSetAddForm.username.trim()==''){
    ElMessage.error("请输入用户名")
  }else if (dataSetAddForm.password.trim()==''){
    ElMessage.error("请输入密码")
  }else {
    axios.post("api/sign/addUser/",{
      username:dataSetAddForm.username,
      password:dataSetAddForm.password
    }).then((res)=>{
      if (res!=400){
        ElMessage.success("添加成功")

      }
      dialogFormVisible.value=false
      dataSetAddForm.username=''
      dataSetAddForm.password=''
      init()
    })
  }
}

const deleteWorker = (row) =>{
  ElMessageBox.confirm(
      '这个操作将会删除账号'+row.name+', 是否继续?',
      '警告',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  )
      .then(() => {
        axios.post("api/sign/delUser/",{
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

const formatTime = (row) =>{
  if (row.last_login==null){
    return "暂未登录"
  }else{
    return row.last_login
  }
}
init()
</script>

<template>
  <div>
    <el-card>
      <div style="margin-bottom: 20px">
        <el-input type="text" v-model="searchName" placeholder="标注人员名称" style="width: 200px;"></el-input>
        <el-button type="primary" @click="SearchDataSet" style="margin-left: 20px">搜索</el-button>
        <el-button type="primary" @click="openAddForm" style="float: right">创建账号</el-button>
      </div>
      <el-table
          :data="dataset"
          :header-cell-style="{'text-align':'center'}"
          :cell-style="{'text-align':'center'}"
          border>
        <el-table-column
            prop="name"
            label="用户名"
            width="200">
        </el-table-column>
        <el-table-column
            prop="last_login"
            label="上次登录"
            width="300"
            :formatter="formatTime">
        </el-table-column>

        <el-table-column
            label="操作"
            width="auto">
          <template style="display: flex" v-slot="scope">
            <el-button  @click="jump(scope.row)" type="primary" round>重置密码</el-button>
            <el-button  @click="deleteWorker(scope.row)" type="danger" round>删除账号</el-button>
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

    <el-dialog v-model="dialogFormVisible" title="创建账号" width="30%" :close-on-click-modal = false>
      <el-form :model="dataSetAddForm" label-position="left">
        <el-form-item label="用户名" label-width="100px">
          <el-input type="text" v-model="dataSetAddForm.username" placeholder="用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" label-width="100px">
          <el-input type="text" v-model="dataSetAddForm.password" placeholder="密码"></el-input>
        </el-form-item>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addUser">确 定</el-button>
      </div>
    </el-dialog>

  </div>

</template>

<style scoped>

</style>