<script lang="ts" setup>
import {reactive, ref} from "vue";
import axios from "axios";
import {ElMessage, ElMessageBox, UploadProps, UploadUserFile} from "element-plus";
import { UploadFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

//首先在setup中定义
const router = useRouter()
const has_data = ref(false)
let dataset = ref([])
const searchName = ref("")

const total=ref(0)
// searchData-向后端分页查询的对象，即当前页和每页总数
const searchData=reactive({
  current:1,
  limit:6
})
const init = ()=>{
  axios.get("api/requester/getDataSetTask").then((res)=>{
    if (res[0]!=null){
      has_data.value = true
      dataset.value = res.slice(0,searchData.limit)
      total.value = res.length
    }else{
      has_data.value = false
    }
  })
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


const getData = (currentPage) =>{
  console.log(currentPage)
  axios.get("api/requester/getDataSetTask").then((res)=>{
    dataset.value = res.slice(searchData.limit*(currentPage-1),searchData.limit*currentPage)
    searchData.current=currentPage
  })
}

init()
</script>

<template>
  <div>
    <el-card>
      <div style="margin-bottom: 20px">
        <el-input type="text" v-model="searchName" placeholder="数据集名称" style="width: 200px;"></el-input>
        <el-button type="primary" @click="SearchDataSet" style="margin-left: 20px">搜索</el-button>

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
            width="200">
        </el-table-column>

        <el-table-column
            label="操作"
            width="auto">
          <template style="display: flex" v-slot="scope">
            <el-button  @click="jump(scope.row)" type="primary" round>开始标注任务</el-button>

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

</template>

<style scoped>

</style>