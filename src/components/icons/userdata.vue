<script setup>
import { ElMessage } from "element-plus";
import axios from "axios";
import { inject, onMounted,ref } from "vue";
const api=inject('api')
let datalist=ref([])

const fetchUserData = async () => {
  try {
    const response = await axios.get('http://localhost:8888/api/userinfo');
    console.log('Response:', response); 
    if (response.data.status === 200) {
      datalist.value = response.data.data;
      console.log('User Data:', datalist.value); 
    } else {
      ElMessage.error(`获取用户数据失败: ${response.data.message}`);
    }
  } catch (error) {
    console.error('请求失败:', error);
    ElMessage.error('请求失败');
  }
};

onMounted(() => {
  fetchUserData(); 
});
</script>
<template>
    <div class="main">
      <div class="center">
        <el-table :data="datalist" style="width: 100%;margin-top: 20px;;" stripe border :cell-style="{ textAlign: 'center' }" :header-cell-style="{ 'text-align': 'center' }" height="100%"
        fit="false">
        <el-table-column type="index" label="序号" width="100">
      </el-table-column>
            <el-table-column  prop="name" label="昵称" width="195" />
            <el-table-column prop="message" label="邮箱" width="195" />
            <el-table-column prop="work_place" label="个人介绍" width="245" />
            <el-table-column prop="reservation_phone" label="用户权限" width="195"/>
        </el-table>
      </div>
    </div>
</template>
<style scoped>
.main{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.center{
    margin-top: 10px;

}
</style>