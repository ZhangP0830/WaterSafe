<script setup>
import { ref, computed } from "vue";

// 任务数据
const tasks = ref([
  {
    id: 1,
    text: "Stop drinking suspicious tap water",
    timeframe: "Right now — Urgent",
    urgency: "URGENT",
    urgencyColor: "danger"
  },
  {
    id: 2,
    text: "Switch infant feeding and formula to bottled water",
    timeframe: "Right now — Urgent",
    urgency: "URGENT",
    urgencyColor: "danger"
  },
  {
    id: 3,
    text: "Check water's color/odor; avoid high-risk uses",
    timeframe: "Within 1 hour — Soon",
    urgency: "SOON",
    urgencyColor: "warning"
  },
  {
    id: 4,
    text: "Prepare bottled water or clean storage containers",
    timeframe: "Within 2 hours — Soon",
    urgency: "SOON",
    urgencyColor: "warning"
  }
]);

// 计算进度
const progress = computed(() => {
  const completed = tasks.value.filter(task => task.completed).length;
  const total = tasks.value.length;
  return {
    percentage: Math.round((completed / total) * 100),
    completed,
    total
  };
});

// 切换任务状态
const toggleTask = (taskId) => {
  const task = tasks.value.find(t => t.id === taskId);
  if (task) {
    task.completed = !task.completed;
  }
};

// 重置所有任务
const resetAll = () => {
  tasks.value.forEach(task => {
    task.completed = false;
  });
};

// 完成所有任务
const completeAll = () => {
  tasks.value.forEach(task => {
    task.completed = true;
  });
};
</script>

<template>
  <div class="card border-0 shadow-sm">
    <div class="card-body p-4">
      <!-- 标题区域 -->
      <div class="d-flex align-items-center mb-4">
        <div class="flex-grow-1">
          <h3 class="mb-1">
            <i class="material-icons text-warning me-2">warning</i>
            Early Signs of Contamination
          </h3>
          <p class="text-muted mb-2">Water quality may be compromised, but no official notice yet.</p>
          <div class="d-flex align-items-center text-muted">
            <i class="material-icons me-1" style="font-size: 1rem;">schedule</i>
            <small>Monitor water quality changes</small>
          </div>
        </div>
        <div class="text-end">
          <div class="h4 mb-0 text-warning">{{ progress.percentage }}%</div>
          <small class="text-muted">{{ progress.completed }}/{{ progress.total }} complete</small>
        </div>
      </div>
      
      <!-- 警告框 -->
      <div class="alert alert-warning d-flex align-items-start mb-4">
        <i class="material-icons me-2 mt-1">warning</i>
        <div>
          <strong>Important:</strong> Stay alert to changes in water quality and prioritize safe drinking options for pregnant women and infants.
        </div>
      </div>
      
      <!-- 任务列表 -->
      <div class="task-list">
        <div 
          v-for="task in tasks" 
          :key="task.id"
          class="task-item d-flex align-items-start p-3 border rounded mb-2"
          :class="{ 'bg-light': task.completed }"
          @click="toggleTask(task.id)"
        >
          <div class="form-check me-3 mt-1">
            <input 
              class="form-check-input" 
              type="checkbox" 
              :id="'advisory-lifted-task-' + task.id"
              :checked="task.completed"
              @click.stop
            >
          </div>
          <div class="flex-grow-1">
            <div 
              class="form-check-label mb-1"
              :class="{ 'text-decoration-line-through text-muted': task.completed }"
            >
              {{ task.text }}
            </div>
            <div class="d-flex align-items-center">
              <small class="text-muted me-2">
                <i class="material-icons me-1" style="font-size: 0.875rem;">schedule</i>
                {{ task.timeframe }}
              </small>
              <span 
                class="badge"
                :class="{
                  'bg-danger': task.urgency === 'URGENT',
                  'bg-warning': task.urgency === 'SOON',
                  'bg-info': task.urgency === 'WHEN POSSIBLE'
                }"
              >
                {{ task.urgency }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 底部操作区域 -->
      <div class="d-flex justify-content-between align-items-center mt-4 pt-3 border-top">
        <div class="text-muted">
          Progress: {{ progress.completed }}/{{ progress.total }} tasks
        </div>
        <div class="btn-group">
          <button @click="resetAll" class="btn btn-outline-secondary btn-sm">
            Reset
          </button>
          <button @click="completeAll" class="btn btn-success btn-sm">
            Complete All
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task-item {
  transition: all 0.3s ease;
  cursor: pointer;
}

.task-item:hover {
  background-color: #f8f9fa;
}

.task-item.bg-light {
  opacity: 0.7;
}

.form-check-input:checked {
  background-color: #198754;
  border-color: #198754;
}

.badge {
  font-size: 0.75rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .task-item {
    padding: 0.75rem !important;
  }
  
  .btn-group .btn {
    font-size: 0.875rem;
    padding: 0.375rem 0.75rem;
  }
}
</style>
