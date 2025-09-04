<script setup>
import { ref, computed } from "vue";

// tasks data
const tasks = ref([
  { id: 1, text: "Run all taps for several minutes to flush pipes", time: "Within 1 hour — Safe", tag: "SAFE", completed: false },
  { id: 2, text: "Wash and disinfect bottles, utensils, and storage containers", time: "Within 2 hours — Safe", tag: "SAFE", completed: false },
  { id: 3, text: "Discard any stored water older than 48 hours", time: "Within 24 hours — Safe", tag: "SAFE", completed: false },
  { id: 4, text: "Inform family and caregivers it's safe to use tap water again", time: "Within 24 hours — Safe", tag: "SAFE", completed: false }
]);

// calculate progress
const progress = computed(() => {
  const completed = tasks.value.filter(task => task.completed).length;
  return {
    count: completed,
    total: tasks.value.length,
    percentage: Math.round((completed / tasks.value.length) * 100)
  };
});

// toggle task status
const toggleTask = (taskId) => {
  const task = tasks.value.find(t => t.id === taskId);
  if (task) {
    task.completed = !task.completed;
  }
};

// reset all tasks
const resetAll = () => {
  tasks.value.forEach(task => task.completed = false);
};

// complete all tasks
const completeAll = () => {
  tasks.value.forEach(task => task.completed = true);
};
</script>

<template>
  <div class="card border-0 shadow-sm">
    <div class="card-body p-4">
      <!-- title area -->
      <div class="d-flex align-items-center mb-4">
        <div class="flex-grow-1">
          <h3 class="mb-1">
            Contamination Cleared
          </h3>
          <p class="text-muted mb-2">Water has tested safe, but pipes and containers may still hold residue.</p>
        </div>
        <div class="text-end">
          <div class="h4 mb-0 text-success">{{ progress.percentage }}%</div>
          <small class="text-muted">{{ progress.count }}/{{ progress.total }} complete</small>
        </div>
      </div>
      
      <!-- safe tip box -->
      <div class="alert alert-success d-flex align-items-start mb-4">
        <i class="material-icons me-2 mt-1">check_circle</i>
        <div>
          <strong>Safe:</strong> Tap water is now usable, but clean your home system to remove risks.
        </div>
      </div>
      
      <!-- task list -->
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
              :id="'task-' + task.id"
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
                  'bg-success': task.tag === 'SAFE',
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
      
      <!-- bottom operation area -->
      <div class="d-flex justify-content-between align-items-center mt-4 pt-3 border-top">
        <div class="text-muted">
          Progress: {{ progress.count }}/{{ progress.total }} tasks
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
  background-color: #17a2b8;
  border-color: #17a2b8;
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
