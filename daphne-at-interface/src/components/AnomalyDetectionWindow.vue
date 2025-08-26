<template>
  <div id="anomaly-detection">
    <div class="is-title">
      Anomaly Detection
      <span class="tutorialLink">
            <u v-on:click.prevent="detectionTutorial">?</u>
            </span>
      <span class="tutorialLink">&#8287; &#8287;</span>
      <span class="tutorialLink">
                <u v-on:click.prevent="clear">Clear</u>
            </span>
      <span class="tutorialLink">&#8287; &#8287;</span>
      <span class="tutorialLink">
                <u v-on:click.prevent="selectall">Select All</u>
            </span>
    </div>
    <div v-if="(this.symptomsList.length === 0)" class="is-content" style="min-height: 100px">
      No anomalous symptoms detected.
    </div>
    <div v-else class="is-content" style="min-height: 100px">
      <!-- New severity-based table structure -->
      <div class="symptoms-table">
        <!-- Warnings Column -->
        <div class="table-column warnings-column">
          <div class="column-header warnings-header">
            <h3>WARNINGS</h3>
          </div>
          <div class="severity-section">
            <div class="section-header">Upper</div>
            <ul v-if="warningsUpper.length > 0">
              <li v-for="symptom in warningsUpper" 
                  :key="symptom.originalIndex"
                  @click="selectSymptom(symptom)"
                  :class="{ 'selected': isSymptomSelected(symptom) }"
                  class="symptom-item warning-item">
                {{ symptom.display_name }}
              </li>
            </ul>
            <div v-else class="empty-state">No warnings detected</div>
          </div>
          <div class="severity-section">
            <div class="section-header">Lower</div>
            <ul v-if="warningsLower.length > 0">
              <li v-for="symptom in warningsLower" 
                  :key="symptom.originalIndex"
                  @click="selectSymptom(symptom)"
                  :class="{ 'selected': isSymptomSelected(symptom) }"
                  class="symptom-item warning-item">
                {{ symptom.display_name }}
              </li>
            </ul>
            <div v-else class="empty-state">No warnings detected</div>
          </div>
        </div>

        <!-- Cautions Column -->
        <div class="table-column cautions-column">
          <div class="column-header cautions-header">
            <h3>CAUTIONS</h3>
          </div>
          <div class="severity-section">
            <div class="section-header">Upper</div>
            <ul v-if="cautionsUpper.length > 0">
              <li v-for="symptom in cautionsUpper" 
                  :key="symptom.originalIndex"
                  @click="selectSymptom(symptom)"
                  :class="{ 'selected': isSymptomSelected(symptom) }"
                  class="symptom-item caution-item">
                {{ symptom.display_name }}
              </li>
            </ul>
            <div v-else class="empty-state">No cautions detected</div>
          </div>
          <div class="severity-section">
            <div class="section-header">Lower</div>
            <ul v-if="cautionsLower.length > 0">
              <li v-for="symptom in cautionsLower" 
                  :key="symptom.originalIndex"
                  @click="selectSymptom(symptom)"
                  :class="{ 'selected': isSymptomSelected(symptom) }"
                  class="symptom-item caution-item">
                {{ symptom.display_name }}
              </li>
            </ul>
            <div v-else class="empty-state">No cautions detected</div>
          </div>
        </div>

        <!-- Outliers Column -->
        <div class="table-column outliers-column">
          <div class="column-header outliers-header">
            <h3>OUTLIERS</h3>
          </div>
          <div class="severity-section">
            <div class="section-header">Upper</div>
            <ul v-if="outliersUpper.length > 0">
              <li v-for="symptom in outliersUpper" 
                  :key="symptom.originalIndex"
                  @click="selectSymptom(symptom)"
                  :class="{ 'selected': isSymptomSelected(symptom) }"
                  class="symptom-item outlier-item">
                {{ symptom.display_name }}
              </li>
            </ul>
            <div v-else class="empty-state">No outliers detected</div>
          </div>
          <div class="severity-section">
            <div class="section-header">Lower</div>
            <ul v-if="outliersLower.length > 0">
              <li v-for="symptom in outliersLower" 
                  :key="symptom.originalIndex"
                  @click="selectSymptom(symptom)"
                  :class="{ 'selected': isSymptomSelected(symptom) }"
                  class="symptom-item outlier-item">
                {{ symptom.display_name }}
              </li>
            </ul>
            <div v-else class="empty-state">No outliers detected</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  name: "AnomalyDetectionWindow",

  data: function () {
    return {
      flash: false,
    }
  },

  computed: {
    ...mapGetters({
      symptomsList: 'getSymptomsList',
      selectedSymptomsList: 'getSelectedSymptomsList',
      selectedLeftSymptoms: 'getSelectedLeftSymptomsList',
      selectedRightSymptoms: 'getSelectedRightSymptomsList'
    }),
    symptomsListLeftColumn() {
      let aux = [];
      let symptomsList = this.symptomsList;
      for (let i = 0; i < symptomsList.length; i = i + 2) {
        aux.push(symptomsList[i]);
      }
      return aux;
    },
    symptomsListRightColumn() {
      let aux = [];
      let symptomsList = this.symptomsList;
      for (let i = 1; i < symptomsList.length; i = i + 2) {
        aux.push(symptomsList[i]);
      }
      return aux;
    },
    // New computed properties for the table structure
    groupedSymptoms() {
      return {
        warnings: {
          upper: this.symptomsList
            .map((symptom, index) => ({ ...symptom, originalIndex: index }))
            .filter(s => s.threshold_tag === 'UpperWarningLimit'),
          lower: this.symptomsList
            .map((symptom, index) => ({ ...symptom, originalIndex: index }))
            .filter(s => s.threshold_tag === 'LowerWarningLimit')
        },
        cautions: {
          upper: this.symptomsList
            .map((symptom, index) => ({ ...symptom, originalIndex: index }))
            .filter(s => s.threshold_tag === 'UpperCautionLimit'),
          lower: this.symptomsList
            .map((symptom, index) => ({ ...symptom, originalIndex: index }))
            .filter(s => s.threshold_tag === 'LowerCautionLimit')
        },
        outliers: { 
          upper: [], 
          lower: [] 
        }
      };
    },
    // Helper computed properties for easier access
    warningsUpper() {
      return this.groupedSymptoms.warnings.upper;
    },
    warningsLower() {
      return this.groupedSymptoms.warnings.lower;
    },
    cautionsUpper() {
      return this.groupedSymptoms.cautions.upper;
    },
    cautionsLower() {
      return this.groupedSymptoms.cautions.lower;
    },
    outliersUpper() {
      return this.groupedSymptoms.outliers.upper;
    },
    outliersLower() {
      return this.groupedSymptoms.outliers.lower;
    }
  },

  methods: {
    leftToggleFontWeight(index, symptom) {
      if (this.isLeftSelected(index)) {
        // Remove symptom
        const filteredSymptoms = this.selectedLeftSymptoms.filter(item => item.index !== index);
        this.$store.commit('mutateSelectedLeftSymptomsList', filteredSymptoms);
        this.$store.dispatch('removeSelectedSymptom', symptom);
      } else {
        // Add symptom
        const updatedSymptoms = [...this.selectedLeftSymptoms, {index: index, symptom: symptom}];
        this.$store.commit('mutateSelectedLeftSymptomsList', updatedSymptoms);
        this.$store.dispatch('addSelectedSymptom', symptom);
      }
    },
    isLeftSelected(index) {
      console.log(this.selectedLeftSymptoms);
      if(this.selectedLeftSymptoms!==undefined)
      return this.selectedLeftSymptoms.some(item => item.index === index);
      return false;
    },
    rightToggleFontWeight(index, symptom) {
      if (this.isRightSelected(index)) {
        // Remove symptom
        const filteredSymptoms = this.selectedRightSymptoms.filter(item => item.index !== index);
        this.$store.commit('mutateSelectedRightSymptomsList', filteredSymptoms);
        this.$store.dispatch('removeSelectedSymptom', symptom);
      } else {
        // Add symptom
        const updatedSymptoms = [...this.selectedRightSymptoms, {index: index, symptom: symptom}];
        this.$store.commit('mutateSelectedRightSymptomsList', updatedSymptoms);
        this.$store.dispatch('addSelectedSymptom', symptom);
      }
    },
    isRightSelected(index) {
      if(this.selectedRightSymptoms!==undefined)
      return this.selectedRightSymptoms.some(item => item.index === index);
      return false;
    },
    selectSymptom(symptom) {
      this.$store.dispatch('addSelectedSymptom', symptom);
    },
    // Helper method for the new table structure to check if a symptom is selected
    isSymptomSelected(symptom) {
      return this.selectedSymptomsList.some(selected => 
        selected.measurement === symptom.measurement &&
        selected.threshold_tag === symptom.threshold_tag
      );
    },
    detectionTutorial(event) {
      this.$root.$emit('detectionTutorialIndividual');
    },
    clear() {
      // Clear all symptoms using mutations
      this.$store.commit('mutateSelectedLeftSymptomsList', []);
      this.$store.commit('mutateSelectedRightSymptomsList', []);
      this.$store.commit('mutateSymptomsList', []);
      this.$store.commit('mutateSelectedSymptomsList', []);
      
      // Update timestamp
      const now = new Date();
      const formattedDate = now.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: true
      });
      this.$store.commit('mutateLastUpdatedSymptomsTimestamp', formattedDate);
    },
    selectall() {
      let symptomsList = this.symptomsList;
      let leftSymptoms = [];
      let rightSymptoms = [];
      let even = 0;
      let odd = 0;
      
      for (let i = 0; i < symptomsList.length; i++) {
        this.$store.dispatch('addSelectedSymptom', symptomsList[i]);
        if (i % 2 === 0) {
          leftSymptoms.push({index: even, symptom: symptomsList[i]});
          even++;
        } else {
          rightSymptoms.push({index: odd, symptom: symptomsList[i]});
          odd++;
        }
      }
      
      // Use mutations to update state
      this.$store.commit('mutateSelectedLeftSymptomsList', leftSymptoms);
      this.$store.commit('mutateSelectedRightSymptomsList', rightSymptoms);
    }
  }
}
</script>

<style scoped>
/* Ensure normal scrolling behavior */
#anomaly-detection {
  position: relative; /* Override any fixed positioning */
  z-index: auto; /* Ensure normal stacking context */
  overflow: visible; /* Allow content to flow normally */
}

li:hover {
  font-weight: bold;
}

/* New table structure styling */
.symptoms-table {
  display: flex;
  gap: 12px; /* Reduced from 20px */
  margin-top: 8px; /* Reduced from 10px */
}

.table-column {
  flex: 1;
  border: 1px solid #444;
  border-radius: 6px; /* Reduced from 8px */
  background: rgba(0, 0, 0, 0.3);
}

.column-header {
  padding: 10px; /* Reduced from 15px */
  text-align: center;
  border-bottom: 1px solid #444;
}

.column-header h3 {
  margin: 0;
  font-size: 1.1em; /* Reduced from 1.2em */
  font-weight: bold;
}

.warnings-header {
  background: #3A0000;
  color: #FF0000;
}

.cautions-header {
  background: #342E00;
  color: #FFBF00;
}

.outliers-header {
  background: #2E2E2E;
  color: #888;
}

.severity-section {
  padding: 10px; /* Reduced from 15px */
  border-bottom: 1px solid #333;
}

.severity-section:last-child {
  border-bottom: none;
}

.section-header {
  font-weight: bold;
  color: #0AFEFF;
  margin-bottom: 8px; /* Reduced from 10px */
  font-size: 0.85em; /* Reduced from 0.9em */
  text-transform: uppercase;
}

.symptom-item {
  cursor: pointer;
  padding: 6px 10px; /* Reduced from 8px 12px */
  margin: 3px 0; /* Reduced from 5px 0 */
  border-radius: 4px;
  transition: all 0.2s ease;
  list-style: none;
}

.symptom-item:hover {
  font-weight: bold;
  background: rgba(255, 255, 255, 0.1);
}

.symptom-item.selected {
  font-weight: bold;
  background: rgba(10, 254, 255, 0.2);
  border: 1px solid #0AFEFF;
}

.warning-item {
  border-left: 3px solid #FF0000;
}

.caution-item {
  border-left: 3px solid #FFBF00;
}

.outlier-item {
  border-left: 3px solid #888;
}

.empty-state {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 12px; /* Reduced from 20px */
  font-size: 0.9em; /* Slightly smaller for empty states */
}

/* Responsive design for smaller screens */
@media (max-width: 768px) {
  .symptoms-table {
    flex-direction: column;
    gap: 10px; /* Reduced from 15px for mobile */
  }
  
  .table-column {
    margin-bottom: 8px; /* Reduced from 10px for mobile */
  }
}
</style>
