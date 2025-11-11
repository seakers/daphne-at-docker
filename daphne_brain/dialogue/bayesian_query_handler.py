import json
import os
from AT.diagnosis.bayesian.ECLSS_Bayesian_Network import get_probabilities
from AT.diagnosis.bayesian.reduce_entropy import calculate_entropy, select_best_evidence
import re

class BayesianQueryHandler:
    """
    Handle queries related to the Bayesian network and probability calculations
    """
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # Get the root directory (daphne_brain app root)
        self.app_root = os.path.dirname(self.current_dir)
        
        # Load probability dictionaries using paths relative to app root
        self.split_probability_dict_path = os.path.join(
            self.app_root, "AT/diagnosis/bayesian/split_probability_dict.json")
        self.hidden_probabilities_dict_path = os.path.join(
            self.app_root, "AT/diagnosis/bayesian/hidden_probabilities_dict.json")
        
        with open(self.split_probability_dict_path, "r") as file:
            self.split_probability_dict = json.load(file)
        with open(self.hidden_probabilities_dict_path, "r") as file:
            self.hidden_probabilities_dict = json.load(file)
    
    def get_hidden_components(self):
        """Return a list of all hidden components in the model"""
        return list(self.hidden_probabilities_dict.keys())
    
    def explain_model_structure(self):
        """Explain the structure of the Bayesian network"""
        # Create a high-level description
        explanation = {
            "voice_message": "The Bayesian network models anomalies and their related measurements and components.",
            "visual_message_type": ["text"],
            "visual_message": [
                "The Bayesian network has three main types of nodes:",
                "1. Anomaly nodes: Represent system anomalies (failures)",
                "2. Measurement nodes: Represent observable telemetry values",
                "3. Hidden component nodes: Represent components that can be inspected, but aren't automatically measured"
            ],
            "writer": "daphne"
        }
        return explanation
    
    def explain_probability_calculation(self):
        """Explain how anomaly probabilities are calculated"""
        explanation = {
            "voice_message": "Anomaly probabilities are calculated using Bayesian inference from observed evidence.",
            "visual_message_type": ["text"],
            "visual_message": [
                "Probabilities are calculated in these steps:",
                "1. Each anomaly has a prior probability (baseline chance of occurrence)",
                "2. Telemetry measurements provide evidence through conditional probability tables",
                "3. For each measurement outside normal ranges, the model updates probabilities",
                "4. Additional evidence from component inspections further updates probabilities",
                "5. A Variable Elimination algorithm calculates the posterior probabilities",
                "6. Results are normalized to sum to 1.0"
            ],
            "writer": "daphne"
        }
        return explanation
        
    def what_if_evidence(self, current_telemetry, current_evidence, additional_evidence_user):
        """
        Calculate how probabilities would change if we add evidence about a component
        
        Args:
            current_telemetry: Current telemetry values
            component: The hidden component to add evidence for
            state: The state of the component (True/False for present/absent)
        
        Returns:
            Updated probabilities and a comparison to previous probabilities
        """
        # Check if component is valid
        print("component for bayesian query", additional_evidence_user)
        

        # Get current probabilities without the new evidence
        print("current evidence for bayesian query", current_evidence)
        print("current telemetry for bayesian query", current_telemetry)
        
        current_probs, _, _ = get_probabilities(current_telemetry, current_evidence)
        print("current probs for bayesian query", current_probs)
        
        # Create evidence dictionary with the new component evidence
        additional_evidence = current_evidence.copy()
        for i in additional_evidence_user:
            additional_evidence[i] = additional_evidence_user[i]

        print("additional evidence for bayesian query", additional_evidence)
        
        # Calculate new probabilities with the added evidence
        new_probs, _, _ = get_probabilities(current_telemetry, additional_evidence)
        print("new probs for bayesian query", new_probs)
        
        top_5_probabilities = dict(sorted(new_probs.items(), 
                                     key=lambda item: item[1], 
                                     reverse=True)[:5])
        # Find the top 5 anomalies with the biggest changes
        changes = {}
        for anomaly in current_probs:
            if anomaly in new_probs:
                changes[anomaly] = new_probs[anomaly] - current_probs[anomaly]
        
        top_changes = sorted(changes.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
        print("top changes for bayesian query", top_changes)
        
        # Create response with comparison
        evidence_list = []
        for component, state in additional_evidence_user.items():
            evidence_list.append(f"{component}")

        # Format the evidence as a readable string
        evidence_display = ", ".join(evidence_list) if evidence_list else "None"

        # Create response with both the evidence and new probabilities
        formatted_probabilities = "\n".join([f"{anomaly}: {prob:.4f}" for anomaly, prob in top_5_probabilities.items()])
        visual_message = [f"If this evidence is added: {evidence_display}\n\nThe new probabilities would be:\n{formatted_probabilities}"]
                
        # for anomaly, change in top_changes:
        #     direction = "increase" if change > 0 else "decrease"
        #     visual_message.append(f"{anomaly}: {current_probs[anomaly]:.4f} → {new_probs[anomaly]:.4f} ({direction} by {abs(change):.4f})")
        
        return {
            "voice_message": f"Adding the evidence would change anomaly probabilities.",
            "visual_message_type": ["text"],
            "visual_message": visual_message,
            "writer": "daphne",
            "options": ["Add to Diagnosis History"],
            "optionsCallbackEvent": "addHypotheticalDiagnosis",
            "hypothetical_data": {
                "probabilities": new_probs,
                "additional_evidence": additional_evidence_user,
                "diagnosis_list": [{
                    "anomaly": anomaly,
                    "probability": prob
                } for anomaly, prob in top_5_probabilities.items()]
            }
        }
    
    def best_evidence_to_collect(self, current_telemetry, current_evidence):
        """
        Determine which evidence would be most informative to collect next
        
        Args:
            current_telemetry: Current telemetry values
        
        Returns:
            Information about the most informative evidence to collect
        """
        # Get current probabilities and the best evidence
        _, best_evidence, hidden_components = get_probabilities(current_telemetry, current_evidence)
        
        if not best_evidence:
            return {
                "voice_message": "No additional evidence would significantly improve diagnostic confidence.",
                "visual_message_type": ["text"],
                "visual_message": ["No additional evidence would significantly improve diagnostic confidence with the current telemetry values."],
                "writer": "daphne"
            }
        
        # Get the anomaly associated with this evidence
        associated_anomalies = []
        for anomaly, data in self.hidden_probabilities_dict.get(best_evidence, {}).items():
            associated_anomalies.append(anomaly)
        
        # Create response
        return {
            "voice_message": f"Collecting evidence about {best_evidence} would be most informative.",
            "visual_message_type": ["text"],
            "visual_message": [
                f"The most informative evidence to collect next is: {best_evidence}",
                f"This component is associated with anomalies: {', '.join(associated_anomalies)}",
                "Checking this component would reduce uncertainty the most in the current diagnosis."
            ],
            "writer": "daphne"
        }
    
    def explain_evidence_impact(self, anomaly):
        """
        Explain which evidence has the most impact on a specific anomaly
        
        Args:
            anomaly: The anomaly to explain evidence for
        
        Returns:
            Explanation of what evidence most affects this anomaly
        """
        relevant_components = []
        
        # Find hidden components related to this anomaly
        for component, anomalies in self.hidden_probabilities_dict.items():
            if anomaly in anomalies:
                relevant_components.append(component)
        
        # Find measurements related to this anomaly
        relevant_measurements = []
        for measurement, anomalies in self.split_probability_dict.items():
            if anomaly in anomalies:
                relevant_measurements.append(measurement)
        
        return {
            "voice_message": f"Several pieces of evidence affect the probability of {anomaly}.",
            "visual_message_type": ["text"],
            "visual_message": [
                f"Evidence that affects {anomaly} probability:",
                f"Hidden components: {', '.join(relevant_components[:5])}{'...' if len(relevant_components) > 5 else ''}",
                f"Measurements: {', '.join(relevant_measurements[:5])}{'...' if len(relevant_measurements) > 5 else ''}"
            ],
            "writer": "daphne"
        }
    
    def handle_query(self, query, current_telemetry, current_evidence=None):
        """
        Main method to handle various Bayesian queries using LLM for intent classification
        
        Args:
            query: The user's query text
            current_telemetry: Current telemetry values
            current_evidence: Any additional evidence already collected
            
        Returns:
            Response to the query
        """
        # Use LLM to classify the query intent
        intent = self.classify_query_intent(query)
        print("intent for bayesian query", intent)
        
        # Handle different types of intents based on LLM classification
        if intent == "probability_calculation_explanation":
            return self.explain_probability_calculation()
            
        elif intent == "model_structure_explanation":
            return self.explain_model_structure()
            
        elif intent == "what_if_evidence":
            # Extract component and state from query using LLM
            additional_evidence = self.extract_component_and_state(query)
            
            if additional_evidence:
                # Check if component exists in our model
                return self.what_if_evidence(current_telemetry, current_evidence, additional_evidence)
    
            else:
                return {
                    "voice_message": "I need to know which component you're asking about.",
                    "visual_message_type": ["text"],
                    "visual_message": [
                        "To answer 'what if' queries, I need to know which component you're asking about.",
                        "For example: 'What if CDRA Failure Component showed damage?'",
                        "Available components include: " + ", ".join(list(self.hidden_probabilities_dict.keys())[:3]) + "..."
                    ],
                    "writer": "daphne"
                }
                
        elif intent == "best_evidence":
            return self.best_evidence_to_collect(current_telemetry, current_evidence)
            
        elif intent == "evidence_impact":
            # Extract anomaly from query using LLM
            anomaly = self.extract_anomaly(query)
            
            if anomaly:
                return self.explain_evidence_impact(anomaly)
            else:
                return {
                    "voice_message": "I need to know which anomaly you're asking about.",
                    "visual_message_type": ["text"],
                    "visual_message": [
                        "To explain evidence impact, I need to know which anomaly you're interested in.",
                        "For example: 'What evidence affects CDRA Failure probability?'"
                    ],
                    "writer": "daphne"
                }
                
        else:
            # Default response for unrecognized Bayesian queries
            return {
                "voice_message": "I can answer questions about the Bayesian diagnosis model.",
                "visual_message_type": ["text"],
                "visual_message": [
                    "I can answer questions about the Bayesian diagnosis model, such as:",
                    "- How are the anomaly probabilities calculated?",
                    "- What would happen if we add evidence that a component is damaged?",
                    "- What's the most informative evidence to collect next?",
                    "- Which evidence has the biggest impact on a specific anomaly?"
                ],
                "writer": "daphne"
            }

    def classify_query_intent(self, query):
        """
        Use LLM to classify the intent of a Bayesian network query
        
        Args:
            query: The user's query text
            
        Returns:
            Classified intent string
        """
        from openai import OpenAI
        import os
        
        # Initialize the OpenAI client with API key from environment
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        print("query for bayesian query", query)
        
        # Prepare the prompt for intent classification
        prompt = f"""
        Classify the following user query about a Bayesian network diagnostic system into one of these categories:
        - probability_calculation_explanation: Questions about how probabilities are calculated
        - model_structure_explanation: Questions about the structure of the Bayesian network
        - what_if_evidence: Questions about hypothetical scenarios like what if i add eveidence that something is damaged, or what if this evidence was added or how would the probabilities change if this evidence was removed and so on
        - best_evidence: Questions about what evidence would be most informative to collect
        - evidence_impact: Questions about which evidence impacts specific anomalies

        Only classify the query into one of these categories. Return only one word in probability_calculation_explanation, model_structure_explanation, what_if_evidence, best_evidence, evidence_impact.
        
        Query: {query}
        
        Return only the category name without explanation.
        """
        
        try:
            # Call the LLM API for classification
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,  # Low temperature for consistent responses
                max_tokens=20     # We only need a short response
            )
            
            # Extract and return the classified intent
            intent = response.choices[0].message.content.strip().lower()

            print("intent for bayesian query", intent)

            return intent
            
        except Exception as e:
            print(f"Error in LLM classification: {e}")
            # Default to 'other' in case of errors
            return 'other'

    def extract_component_and_state(self, query):
        """
        Use LLM to extract component name and state from a query
        
        Args:
            query: The user's query text
            
        Returns:
            Tuple of (component_name, state_boolean)
        """
        from openai import OpenAI
        import os
        
        # Initialize the OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Get list of valid components to include in prompt
        valid_components = list(self.hidden_probabilities_dict.keys())  # Limit to 10 for reasonable prompt size
        
        # Prepare the prompt for entity extraction
        prompt = f"""
        Extract the component name and its state from the following query about a Bayesian network.
        The query is asking what would happen if a particular component had evidence indicating it was in a particular state.
        
        Valid components include: {', '.join(valid_components)}
        
        Query: {query}
        
        For the state values, map them according to these rules:
        - Map to "true" if the user says: damaged, positive, present, abnormal, fault, failure, or values 3, 4, 5
        - Map to "false" if the user says: undamaged, negative, absent, normal, intact, working, operational, or values 1, 2
        
        Output format:
        Return the output in JSON format of component names and states in the format - "component name1": "state1", "component name2": "state2" and so on.`
    
        Make sure to match the users component to the one in the list and return that exact name from the list. Make sure to include the [HIDDEN] in the name as in the list. DONOT change anything.
    
        DONOT return anything else only the JSON.
        """
        
        try:
            # Call the LLM API for entity extraction
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,  # Low temperature for consistent responses
                max_tokens=100    # Limit response length
            )
            
            # Extract the information from the response
            result_text = response.choices[0].message.content.strip()
            result_text = re.sub(r'```(\w+)?\s*', '', result_text)
            result_text = re.sub(r'\s*```', '', result_text)
            print("result text for bayesian query", result_text)
            
            # Parse the result
            additional_evidence = {}
            
            json_data = json.loads(result_text)
            if json_data:
                for key, value in json_data.items():
                    # Check if the component is valid
                    if key in valid_components:
                        additional_evidence[key] = 4 if value.lower() == "true" else 1
            
            return additional_evidence
            
        except Exception as e:
            print(f"Error in LLM entity extraction: {e}")
            return None, True

    def extract_anomaly(self, query):
        """
        Use LLM to extract anomaly name from a query
        
        Args:
            query: The user's query text
            
        Returns:
            Extracted anomaly name or None if not found
        """
        from openai import OpenAI
        import os
        
        # Initialize the OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Collect all anomalies from the probability dictionaries
        all_anomalies = set()
        for anomalies in self.split_probability_dict.values():
            all_anomalies.update(anomalies.keys())
        
        # Convert to list for the prompt
        anomaly_list = list(all_anomalies)[:20]  # Limit to 20 for reasonable prompt size
        
        # Prepare the prompt for entity extraction
        prompt = f"""
        Extract the anomaly name from the following query about evidence impact in a Bayesian network.
        The query is asking which evidence affects a particular anomaly's probability.
        
        Valid anomalies include: {', '.join(anomaly_list)}
        
        Query: {query}
        
        Output format:
        Anomaly: [exact anomaly name from the list or NONE if not found]
        """
        
        try:
            # Call the LLM API for entity extraction
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,  # Low temperature for consistent responses
                max_tokens=50     # Limit response length
            )
            
            # Extract the information from the response
            result_text = response.choices[0].message.content.strip()
            
            # Parse the result
            anomaly = None
            
            for line in result_text.split('\n'):
                if line.lower().startswith('anomaly:'):
                    anomaly = line[len('anomaly:'):].strip()
                    if anomaly.upper() == 'NONE':
                        anomaly = None
                    break
            
            return anomaly
            
        except Exception as e:
            print(f"Error in LLM entity extraction: {e}")
            return None