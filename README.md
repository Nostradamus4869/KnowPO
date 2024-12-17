# KnowPO: Knowledge-aware Preference Optimization for Controllable Knowledge Selection in Retrieval-Augmented Language Models

Welcome to the official repository for *KnowPO: Knowledge-aware Preference Optimization for Controllable Knowledge Selection in Retrieval-Augmented Language Models*.

**📢 News: this work has been accepted at the AAAI 2025 !**

If you find this project useful, please consider **giving us a ⭐️**! Your support is a great encouragement for us.

---

## 📋 **Requirements**

This repository provides scripts for data processing and construction. There are **no strict environment requirements** — feel free to use your preferred environment.

---

## 🚀 **Usage**

### **1. Prepare Dataset**

#### **Step 1: Download Raw Datasets**

We cannot directly provide the **SQuAD2.0** and **SQuAD2.0 Chinese** datasets. You must download them manually from the following sources:

- [SQuAD2.0 Official Website](https://rajpurkar.github.io/SQuAD-explorer/)
- [Chinese-SQuAD GitHub Repository](https://github.com/junzeng-pluto/ChineseSquad)

After downloading the datasets, move the data files to the following directory:

```bash
data/SquadZen/raw/
```

Run the following script to process the raw datasets:

```bash
python process.py
```

⚠️ **Important**: Modify the file path in the script to point to your downloaded dataset:

```python
filename = '/path/to/train-zen-v1.0.json'
```

This step reorganizes the questions and corpus from the dataset.

---

#### **Step 2: Data Preprocessing**

Run the following preprocessing script:

```bash
bash data_preprocessing/data_preprocessing.sh
```

The individual scripts perform the following tasks:

| **Script**                               | **Description**                                              |
| ---------------------------------------- | ------------------------------------------------------------ |
| `generate_inner_answer.py`               | Extracts **parameter answer** from a local pre-trained model. |
| `generate_counterfactual.py`             | Uses OpenAI models to generate **fabricated answers**.       |
| `generate_context.py`                    | Constructs **counterfactual documents** by replacing realistic answers with fabricated ones. |
| `generate_IR.py` and `generate_RandC.py` | Generate context types discussed in **Section III.C** of our paper. |
| `generate_negative.py`                   | Uses OpenAI models to construct **Contextual Overinclusion** and **Contextual Ignorance** error types. |

> **Example Processed Data**: We provide sample processed data under the `data/SquadZen/processed` directory for reference.

---

#### **Step 3: Generate Training Datasets**

Generate datasets for the **Supervised Fine-Tuning (SFT)** and **Direct Preference Optimization (DPO)** phases:

```bash
python generate_sft_dataset.py
python generate_dpo_dataset.py
```

> **Example Training Data**: We also provide sample SFT and DPO datasets under the `data/SquadZen/sft` and `data/SquadZen/dpo` directories.

---

### **2. Training**

We use the [**LLaMA-Factory**](https://github.com/hiyouga/LLaMA-Factory) project for training. Once the SFT and DPO datasets are prepared, follow the tutorial in the LLaMA-Factory repository for training:

- Supports command-line, Web UI, and other monitoring interfaces.
- **Special thanks to** the LLaMA-Factory team for their support and open-source contribution.

Alternatively, you can use any other framework of your choice for model training.

---

## 📖 **Related Paper**

For more technical details, please refer to our paper accepted at **AAAI 2025**.



