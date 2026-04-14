<template>
  <div class="teacher-wrap">
    <h2>教师后台</h2>
    <el-tabs v-model="tab">
      <el-tab-pane label="班级管理" name="class">
        <el-button type="primary" @click="addClass=true">新建班级</el-button>
        <el-table :data="classList" border>
          <el-table-column label="班级" prop="class_name" />
          <el-table-column label="学院" prop="college" />
          <el-table-column label="专业" prop="major" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button @click="loadPapers(scope.row.id)">查看论文</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-dialog v-model="addClass" title="新建班级">
          <el-form v-model="classForm">
            <el-form-item label="名称"><el-input v-model="classForm.name" /></el-form-item>
            <el-form-item label="学院"><el-input v-model="classForm.college" /></el-form-item>
            <el-form-item label="专业"><el-input v-model="classForm.major" /></el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="addClass=false">取消</el-button>
            <el-button type="primary" @click="createClass">确定</el-button>
          </template>
        </el-dialog>
      </el-tab-pane>

      <el-tab-pane label="格式模板" name="template">
        <el-button type="primary" @click="addTpl=true">新建模板</el-button>
        <el-table :data="tplList" border>
          <el-table-column label="模板名" prop="template_name" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button @click="selectTpl(scope.row)">配置规则</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div v-if="currentTpl" style="margin-top:20px">
          <h3>规则：{{currentTpl.template_name}}</h3>
          <el-button type="success" @click="addRule=true">添加规则</el-button>
          <el-table :data="ruleList" border style="margin-top:10px">
            <el-table-column label="对象" prop="target_part" />
            <el-table-column label="规则项" prop="rule_key" />
            <el-table-column label="要求值" prop="rule_value" />
            <el-table-column label="提示" prop="error_tip" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button type="danger" @click="deleteRule(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <el-dialog v-model="addTpl" title="新建模板">
          <el-input v-model="tplName" placeholder="模板名" />
          <template #footer>
            <el-button @click="addTpl=false">取消</el-button>
            <el-button type="primary" @click="createTpl">确定</el-button>
          </template>
        </el-dialog>

        <el-dialog v-model="addRule" title="添加规则">
          <el-form v-model="ruleForm">
            <el-form-item label="检测对象">
              <el-select v-model="ruleForm.target_part">
                <el-option label="正文" value="正文" />
                <el-option label="标题" value="标题" />
                <el-option label="参考文献" value="参考文献" />
              </el-select>
            </el-form-item>
            <el-form-item label="规则项">
              <el-select v-model="ruleForm.rule_key">
                <el-option label="中文字体" value="font_name_zh" />
                <el-option label="英文字体" value="font_name_en" />
                <el-option label="字号" value="font_size" />
                <el-option label="行距" value="line_height" />
                <el-option label="缩进" value="indent" />
              </el-select>
            </el-form-item>
            <el-form-item label="要求值"><el-input v-model="ruleForm.rule_value" /></el-form-item>
            <el-form-item label="错误提示"><el-input v-model="ruleForm.error_tip" /></el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="addRule=false">取消</el-button>
            <el-button type="primary" @click="saveRule">保存</el-button>
          </template>
        </el-dialog>
      </el-tab-pane>

      <el-tab-pane label="论文检测" name="paper">
        <el-table :data="paperList" border>
          <el-table-column label="论文" prop="paper_name" />
          <el-table-column label="上传时间" prop="upload_time" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button @click="doCheck(scope.row.id)">开始检测</el-button>
              <el-button @click="showResult(scope.row.id)">查看报告</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div v-if="result" style="margin-top:20px">
          <h3>检测得分：{{result.task.format_score}}</h3>
          <el-table :data="result.errors" border>
            <el-table-column label="位置" prop="position" />
            <el-table-column label="问题" prop="error_message" />
            <el-table-column label="要求" prop="expect_value" />
            <el-table-column label="实际" prop="actual_value" />
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const tab = ref("class")
const classList = ref([])
const tplList = ref([])
const ruleList = ref([])
const paperList = ref([])
const addClass = ref(false)
const addTpl = ref(false)
const addRule = ref(false)
const currentTpl = ref(null)
const result = ref(null)

const classForm = ref({name:"", college:"", major:""})
const tplName = ref("")
const ruleForm = ref({target_part:"正文", rule_key:"font_name", rule_value:"宋体", error_tip:"字体必须为宋体"})

onMounted(()=>{
  loadClass()
  loadTpl()
})

const loadClass = async ()=>{
  const res = await axios.get("/teacher/class/list")
  classList.value = res.data
}
const createClass = async ()=>{
  await axios.post(`/teacher/class/create?name=${classForm.value.name}&college=${classForm.value.college}&major=${classForm.value.major}`)
  addClass.value = false
  loadClass()
}

const loadTpl = async ()=>{
  const res = await axios.get("/teacher/template/list")
  tplList.value = res.data
}
const createTpl = async ()=>{
  await axios.post(`/teacher/template/create?name=${tplName.value}`)
  addTpl.value = false
  loadTpl()
}
const selectTpl = async (row)=>{
  currentTpl.value = row
  const res = await axios.get(`/teacher/rule/list/${row.id}`)
  ruleList.value = res.data
}
const saveRule = async ()=>{
  await axios.post("/teacher/rule/add", {...ruleForm.value, template_id: currentTpl.value.id})
  addRule.value = false
  selectTpl(currentTpl.value)
}

const deleteRule = async (ruleId)=>{
  if (confirm('确定要删除这条规则吗？')) {
    await axios.delete(`/teacher/rule/delete/${ruleId}`)
    selectTpl(currentTpl.value)
  }
}

const loadPapers = async (cid)=>{
  tab.value = "paper"
  const res = await axios.get(`/teacher/class/${cid}/papers`)
  paperList.value = res.data
}
const doCheck = async (pid)=>{
  const res = await axios.post(`/paper/check/${pid}?template_id=${currentTpl.value.id}`)
  alert("检测完成，得分："+res.data.score)
}
const showResult = async (pid)=>{
  const res = await axios.get(`/paper/result/${pid}`)
  result.value = res.data
}
</script>

<style scoped>
.teacher-wrap{padding:20px;}
</style>