<script setup>
import { ref, computed } from "vue";

// 任务数据
const tasks = ref([
  { id: 1, text: "Immediately stop all drinking and cooking with tap water", time: "Right now — Urgent", tag: "URGENT", completed: false },
  { id: 2, text: "Switch infant and pregnancy use to bottled or emergency water", time: "Right now — Urgent", tag: "URGENT", completed: false },
  { id: 3, text: "Use tap water only for toilet flushing, not for dishes or infant contact", time: "Within 30 minutes — Soon", tag: "SOON", completed: false },
  { id: 4, text: "Collect bottled water or go to designated supply points", time: "Within 2 hours — Soon", tag: "SOON", completed: false }
]);

// 计算进度
const progress = computed(() => {
  const completed = tasks.value.filter(task => task.completed).length;
  return {
    count: completed,
    total: tasks.value.length,
    percentage: Math.round((completed / tasks.value.length) * 100)
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
  tasks.value.forEach(task => task.completed = false);
};

// 完成所有任务
const completeAll = () => {
  tasks.value.forEach(task => task.completed = true);
};
</script>

<template>
  <div class="card border-0 shadow-sm">
    <div class="card-body p-4">
      <!-- 标题区域 -->
      <div class="d-flex align-items-center mb-4">
        <div class="flex-grow-1">
          <h3 class="mb-1">
            Severe Contamination
          </h3>
          <p class="text-muted mb-2">Chemical or toxic contamination present. Boiling is not effective.</p>
        </div>
        <div class="text-end">
          <div class="h4 mb-0 text-danger">{{ progress.percentage }}%</div>
          <small class="text-muted">{{ progress.count }}/{{ progress.total }} complete</small>
        </div>
      </div>
      
      <!-- 警告框 -->
      <div class="alert alert-warning d-flex align-items-start mb-4">
        <i class="material-icons me-2 mt-1">warning</i>
        <div>
          <strong>Important:</strong> Tap water is unsafe for all consumption. Use bottled or emergency supply only.
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
              :id="'do-not-drink-task-' + task.id"
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
                {{ task.time }}
              </small>
              <span 
                class="badge"
                :class="{
                  'bg-danger': task.tag === 'URGENT',
                  'bg-warning': task.tag === 'SOON',
                  'bg-info': task.tag === 'WHEN POSSIBLE'
                }"
              >
                {{ task.tag }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 底部操作区域 -->
      <div class="d-flex justify-content-between align-items-center mt-4 pt-3 border-top">
        <div class="text-muted">
          Progress: {{ progress.count }}/{{ progress.total }} tasks
        </div>
        <div class="btn-group">
          <button @click="resetAll" class="btn btn-outline-secondary btn-sm">
            Reset
          </button>
          <button @click="completeAll" class="btn btn-danger btn-sm">
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
  background-color: #dc3545;
  border-color: #dc3545;
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


