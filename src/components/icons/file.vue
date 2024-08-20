<template>
  <div class="file-container">
    <div class="chat-header">
      <h2>批量检测攻击性和偏见语言</h2>
      <p>上传你的csv文件</p>
    </div>
    <el-upload 
      class="upload"
      drag
      action=""
      :on-change="handleFileChange"
      :auto-upload="false"
      accept=".csv"
    >
      <el-icon size="100"><UploadFilled /></el-icon>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    </el-upload>
    <el-table
      v-if="tableData.length > 0"
      :data="tableData"
      style="width: 80%"
      height="500"
      border
      stripe
    >
      <el-table-column
        v-for="(column, index) in columns"
        :key="index"
        :prop="column"
        :label="column"
      ></el-table-column>
    </el-table>
      <el-select v-if="tableData.length > 0"
        class="select"
        v-model="value" 
        @change="onColumnChange"
        placeholder="请选择你想要检测内容的列名">
        <el-option
         v-for="(column, index) in columns"
         :key="index"
         :label="column"
         :value="column">
        </el-option>
       </el-select>
       <el-table
          v-if="selectedColumnData.length > 0"
          :data="selectedColumnData"
           style="width: 80%"
           height="300">
          <el-table-column 
            prop="value"
            >
          </el-table-column>
         </el-table>
         <el-button
          class="submit-button"
          v-if="selectedColumnData.length > 0"
          type="primary"
          @click="onSubmit"
          >开始检测</el-button>
         <el-table
            v-if="combinedData.length > 0"
            :data="combinedData"
            style="width: 80%"
            height="300"
            border
            stripe
          >
            <el-table-column
              prop="originalData"
              label="检测句子"
          >
            </el-table-column>
          <el-table-column
            prop="responseData"
            label="检测结果"
           >
          </el-table-column>
         </el-table>
         <el-button type="success"
         class="success-button"
          v-if="isDetectionComplete === true"
         >
          检测完成, 是否保存为csv文件
         </el-button>
  </div>
</template>

<script>
import Papa from 'papaparse';
// 后端地址
const API_URL = 'http://localhost:5000/predict';
export default {
  data() {
    return {
      tableData: [],
      columns: [],
      selectedColumnData: [], // 存储选中列的数据
      columnWidths: {},
      isSending: false,
      combinedData: [],
      isDetectionComplete: false,
    };
  },
  methods: {
    handleFileChange(file) {
      const fileReader = new FileReader();
      fileReader.onload = (e) => {
        const csvData = e.target.result;
        Papa.parse(csvData, {
          header: true,
          complete: (results) => {
            this.columns = Object.keys(results.data[0]);
            this.tableData = results.data;
            this.calculateColumnWidths();
          },
        });
      };
      fileReader.readAsText(file.raw);
    },
      onColumnChange(columnName) {
      this.selectedColumnData = this.tableData.map(row => ({ value: row[columnName] }));
    },
    async sendDataToBackend(data) {
      if (this.isSending) return;
      if (this.isDetectionComplete) return;
      this.isSending = true;
      try {
        const response = await fetch(API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({text: data.value}),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const Data = await response.json();
        const responseData = Data.prediction;
        this.handleResponse(data, responseData);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        this.isSending = false;
      }
    },
    handleResponse(originalData, responseData) {
      const combinedItem = {
        originalData: originalData.value, 
        responseData: responseData,
      };
      // 添加到`combinedData`数组中
      this.combinedData.push(combinedItem);
    },
    async onSubmit() {
      for (const item of this.selectedColumnData) {
        await this.sendDataToBackend(item);
      }
      this.isDetectionComplete = true;
    },
  }
};
</script>
<style scoped>
.file-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-right: 20px;
}

.chat-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.upload {
  width: 80%;
  margin-bottom: 10px;
  margin-top: 10px;
}
.select {
  width: 80%;
  margin-bottom: 10px;
  margin-top: 10px;
}
.submit-button {
  width: 80%;
  margin-bottom: 10px;
  margin-top: 10px;
}
.success-button {
  width: 80%;
  margin-bottom: 10px;
  margin-top: 10px;
}
</style>