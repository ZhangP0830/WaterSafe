<script setup>
import { ref, computed } from "vue";

// 任务数据
const tasks = ref([
  {
    id: 1,
    text: "Flush all taps for 3-5 minutes",
    timeframe: "Before first use",
    urgency: "URGENT",
    urgencyColor: "danger"
  },
  {
    id: 2,
    text: "Flush hot water heater by running hot water",
    timeframe: "Before using hot water",
    urgency: "URGENT",
    urgencyColor: "danger"
  },
  {
    id: 3,
    text: "Discard all ice made during advisory",
    timeframe: "Right now",
    urgency: "URGENT",
    urgencyColor: "danger"
  },
  {
    id: 4,
    text: "Clean water-using appliances (coffee maker, etc.)",
    timeframe: "Before next use",
    urgency: "SOON",
    urgencyColor: "warning"
  },
  {
    id: 5,
    text: "Replace any water filters used during advisory",
    timeframe: "Within 24 hours",
    urgency: "SOON",
    urgencyColor: "warning"
  },
  {
    id: 6,
    text: "Gradually transition from bottled to tap water",
    timeframe: "Over 1-2 days",
    urgency: "WHEN POSSIBLE",
    urgencyColor: "info"
  },
  {
    id: 7,
    text: "Restock emergency water supply",
    timeframe: "When convenient",
    urgency: "WHEN POSSIBLE",
    urgencyColor: "info"
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
            <i class="material-icons text-success me-2">check_circle</i>
            Advisory Lifted
          </h3>
          <p class="text-muted mb-2">Water is now safe, but take precautions before returning to normal use.</p>
          <div class="d-flex align-items-center text-muted">
            <i class="material-icons me-1" style="font-size: 1rem;">schedule</i>
            <small>Transition period: 1-2 days</small>
          </div>
        </div>
        <div class="text-end">
          <div class="h4 mb-0 text-success">{{ progress.percentage }}%</div>
          <small class="text-muted">{{ progress.completed }}/{{ progress.total }} complete</small>
        </div>
      </div>
      
      <!-- 警告框 -->
      <div class="alert alert-light border d-flex align-items-start mb-4">
        <i class="material-icons text-light me-2 mt-1">warning</i>
        <div class="text-dark">
          Even though the advisory is lifted, flush your system thoroughly before returning to normal use.
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
