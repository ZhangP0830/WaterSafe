<script setup>
import { ref, computed } from "vue";

// Tasks Data
const tasks = ref([
  { 
    id: 1, 
    text: "Stop using unboiled tap water immediately", 
    time: "Right now — Urgent", 
    tag: "URGENT", 
    completed: false 
  },
  { 
    id: 2, 
    text: "Inform family members and caregivers about boil rules", 
    time: "Right now — Urgent", 
    tag: "URGENT", 
    completed: false 
  },
  { 
    id: 3, 
    text: "Boil and cool water for drinking, brushing teeth, cooking, and formula", 
    time: "Next 30 minutes — Soon", 
    tag: "SOON", 
    completed: false 
  },
  { 
    id: 4, 
    text: "Check bottled water supplies; restock if running low", 
    time: "Within 2 hours — Soon", 
    tag: "SOON", 
    completed: false 
  }
]);

// Calculate Progress
const progress = computed(() => {
  const completed = tasks.value.filter(task => task.completed).length;
  return {
    count: completed,
    total: tasks.value.length,
    percentage: Math.round((completed / tasks.value.length) * 100)
  };
});

// Toggle Task Status
const toggleTask = (taskId) => {
  const task = tasks.value.find(t => t.id === taskId);
  if (task) {
    task.completed = !task.completed;
  }
};

// Reset All Tasks
const resetAll = () => {
  tasks.value.forEach(task => task.completed = false);
};

// Complete All Tasks
const completeAll = () => {
  tasks.value.forEach(task => task.completed = true);
};
</script>

<template>
  <div class="card border-0 shadow-sm">
    <div class="card-body p-4">
      <!-- Title Area-->
      <div class="d-flex align-items-center mb-4">
        <div class="flex-grow-1">
          <h3 class="mb-1">
            Confirmed Contamination
          </h3>
          <p class="text-muted mb-2">Microbial contamination present. All water must be boiled before use.</p>
        </div>
        <div class="text-end">
          <div class="h4 mb-0 text-primary">{{ progress.percentage }}%</div>
          <small class="text-muted">{{ progress.count }}/{{ progress.total }} complete</small>
        </div>
      </div>
      
      <!-- Warning Alert-->
      <div class="alert alert-warning d-flex align-items-start mb-4">
        <i class="material-icons me-2 mt-1">warning</i>
        <div>
          <strong>Important:</strong> Boil all water for at least 1 minute and cool before drinking, cooking, or infant use.
        </div>
      </div>
      
      <!-- Tasks List-->
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
              class="modern-checkbox" 
              type="checkbox" 
              :id="'confirmed-task-' + task.id"
              :checked="task.completed"
              @click.stop="toggleTask(task.id)"
            >
          </div>
          <div class="flex-grow-1">
            <div 
              class="form-check-label mb-2"
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
          <button @click="completeAll" class="btn btn-primary btn-sm">
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

.modern-checkbox {
  width: 24px;
  height: 24px;
  border: 2px solid #dee2e6;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 4px;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  position: relative;
  flex-shrink: 0;
}

.modern-checkbox:hover {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.1);
}

.modern-checkbox:checked {
  background: #28a745;
  border-color: #28a745;
  box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2);
}

.modern-checkbox:checked::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 14px;
  font-weight: bold;
  line-height: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.modern-checkbox:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

.modern-checkbox:checked:focus {
  box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.25);
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
