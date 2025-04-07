<template>
    <div class="modal" :class="{ 'is-active': isActive }">
      <div class="modal-background" @click="cancel"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Select Symptoms for Additional Evidence</p>
          <button class="delete" aria-label="close" @click="cancel"></button>
        </header>
        <section class="modal-card-body">
          <p>Please select all symptoms that you can provide additional information about:</p>
          <div class="symptom-selection">
            <div v-for="symptom in availableSymptoms" :key="symptom" 
                 class="symptom-box" 
                 :class="{ 'selected': selectedSymptoms.includes(symptom) }"
                 @click="toggleSymptom(symptom)">
              {{ symptom }}
            </div>
          </div>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-primary" @click="proceed" :disabled="selectedSymptoms.length === 0">
            Proceed
          </button>
          <button class="button" @click="cancel">Cancel</button>
        </footer>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "SymptomSelectionDialog",
    props: {
      isActive: {
        type: Boolean,
        default: false
      },
      symptoms: {
        type: Array,
        default: () => []
      }
    },
    data() {
      return {
        selectedSymptoms: []
      }
    },
    computed: {
      availableSymptoms() {
        return this.symptoms;
      }
    },
    methods: {
      toggleSymptom(symptom) {
        if (this.selectedSymptoms.includes(symptom)) {
          this.selectedSymptoms = this.selectedSymptoms.filter(s => s !== symptom);
        } else {
          this.selectedSymptoms.push(symptom);
        }
      },
      proceed() {
        this.$emit('proceed', this.selectedSymptoms);
      },
      cancel() {
        this.$emit('cancel');
      }
    }
  }
  </script>
  
  <style scoped>

.modal-background {
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-card {
  background-color: #1c1c1c;
  color: white;
}

.modal-card-head {
  background-color: #002E2E;
  color: white;
  border-bottom: 1px solid #0AFEFF;
}

.modal-card-title {
  color: white;
}

.modal-card-body {
  background-color: #1c1c1c;
  color: white;
}

.modal-card-foot {
  background-color: #1c1c1c;
  border-top: 1px solid #0AFEFF;
}

.symptom-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

.symptom-box {
  padding: 10px 15px;
  border: 1px solid #0AFEFF;
  border-radius: 4px;
  background: #002E2E;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s;
}

.symptom-box:hover {
  background: #003f3f;
  border-color: #0AFEFF;
}

.symptom-box.selected {
  background: #0AFEFF;
  color: #002E2E;
  font-weight: bold;
}

.button.is-primary {
  background-color: #0AFEFF;
  color: #002E2E;
}

.button {
  background-color: #002E2E;
  color: white;
  border: 1px solid #0AFEFF;
}

.button:hover {
  background-color: #003f3f;
}

.delete {
  background-color: #ff5b5b;
}

.delete:hover {
  background-color: #ff3333;
}
  </style>