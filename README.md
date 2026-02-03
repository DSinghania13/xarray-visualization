# Visualization of Shear Force and Bending Moment Diagrams  
### Using Xarray and Plotly (MIDAS-style Post-Processing)

---

## 📌 Submission Details

- **Project Title:** Visualization of Shear Force and Bending Moment Diagrams using Xarray and Plotly
- **Organization:** Osdag (FOSSEE, IIT Bombay)
- **Task Type:** Technical Screening Assignment  
- **Domain:** Structural Engineering / Software Development
<br>

- **Submitted by:** Divit Singhania
- **Program:** B.Tech Computer Science (AI & ML)
- **Institution:** VIT Bhopal University

---

## 🎥 Video Demonstration

A short screen-recorded demonstration of the code execution and generated plots is available below:

> 🔗 **YouTube (Unlisted) Video Link:** > [Paste your YouTube Link Here]

---

## 🧠 Project Overview

This repository contains Python scripts to generate **2D and 3D Shear Force Diagrams (SFD)** and **Bending Moment Diagrams (BMD)** from an **Xarray dataset**, closely replicating **MIDAS Civil post-processing visualizations**.

The project demonstrates:
- Correct use of **FEM element connectivity**
- Accurate **node-based geometric reconstruction**
- Preservation of **sign conventions from the dataset**
- Professional-quality **2D and 3D structural plots**

---

## 📁 Repository Structure

```text
xarray-visualization/
│
├── data/
│   ├── screening_task.nc
│   ├── node.py
│   └── element.py
│
├── scripts/
│   ├── xarray_usage.py
│   ├── task1_2d.py
│   └── task2_3d.py
│
├── figures/
│   ├── dataset_visualization.png
│   ├── node_element_connectivity.png
│   ├── SDF_2D.png
│   ├── BMD_2D.png
│   ├── SDF_3D.png
│   └── BMD_3D.png
│
├── report/
│   └── Report.pdf
│
├── requirements.txt
├── README.md
└── .gitignore

```

---

## 📊 Dataset Description

### `screening_task.nc` (Xarray Dataset)

* **Dimensions**
* `Element` → Beam element IDs
* `Component` → Internal force components


* **Force Components Used**
* `Vy_i`, `Vy_j` → Shear force at start/end node
* `Mz_i`, `Mz_j` → Bending moment at start/end node



**Suffix meaning:**

* `_i` → Start node of element
* `_j` → End node of element

  
![dataset_visualization](https://github.com/user-attachments/assets/8b45906c-2d71-4bc8-a50e-d46fa1bea8f7)

*Figure 1: Xarray dataset structure and force components*

---

## 🧩 Node Coordinates & Element Connectivity

**`node.py`** defines node geometry:

```
node_id → (x, y, z)
```

**`element.py`** defines FEM connectivity:

```
element_id → (start_node, end_node)
```

![node_element_conectivity](https://github.com/user-attachments/assets/ea2b8c48-efcd-46ad-a752-45fa45dde4e3)

*Figure 2: Node coordinates and element connectivity. All plots use actual geometry — no assumed or artificial coordinates.*

---

## 🧪 Scripts Overview

### 1️⃣ `xarray_usage.py`

**Inspects dataset structure**

* Identifies force components.
* Extracts tabular force data for verification.

### 2️⃣ `task1_2d.py` — Task-1 (2D Plots)

Generates **2D Shear Force (SFD)** and **Bending Moment (BMD)** diagrams for the **Central Longitudinal Girder** elements: `[15, 24, 33, 42, 51, 60, 69, 78, 83]`.

**Plotting Logic:**

* **SFD:** Step-wise (constant per element).
* **BMD:** Linear interpolation between nodes.
* **Sign Convention:** Preserved exactly from the dataset.

![SFD_2D](https://github.com/user-attachments/assets/b04a57f5-6e24-4efb-95a6-3d83cfb8d0dd)

*Figure 3: 2D Shear Force Diagram*

![BMD_2D](https://github.com/user-attachments/assets/44a6fb54-d285-4954-aa3f-41c0bdfec316)

*Figure 4: 2D Bending Moment Diagram*

### 3️⃣ `task2_3d.py` — Task-2 (3D MIDAS-Style Plots)

Generates **3D SFD & BMD** for **all five longitudinal girders**.

**Visualization Features:**

* **X:** Bridge length | **Z:** Bridge width | **Y:** Force magnitude (vertical extrusion).
* **Vertical Hatching:** "Fence" style plotting for transparency.
* **Heat-map Coloring:** Jet colormap (Blue → Red) based on magnitude.
* **Global Scaling:** Auto-scaled to maintain visual proportions.

![SFD_3D](https://github.com/user-attachments/assets/6aae3e99-d082-45d2-af98-99188cb22237)

*Figure 5: 3D Shear Force Diagram (SFD) — All Girders*

![BMD_3D](https://github.com/user-attachments/assets/adc02ef5-8ec7-47d9-a4ef-38a52f099afc)

*Figure 6: 3D Bending Moment Diagram (BMD) — All Girders*

---

## ▶️ How to Run the Code

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Navigate to scripts folder
cd scripts

# 3. Run verification script
python xarray_usage.py

# 4. Run Task 1 (2D Plots)
python task1_2d.py

# 5. Run Task 2 (3D Plots)
python task2_3d.py

```

---

## 🧾 Report Documentation

A detailed PDF report is available, covering dataset inspection, code logic, plot construction, and verification against marking criteria.

📄 **Read the Report:** [report/SFD_BMD_Report.pdf](https://www.google.com/search?q=report/SFD_BMD_Report.pdf)

---

## 🛠️ Tech Stack

* **Python 3.11**
* **Xarray** – Dataset handling
* **NumPy** – Numerical operations
* **Plotly** – 2D & 3D visualization
* **netCDF4** – Dataset backend
* **Pandas** - Dataset visualization

---

## ✅ Alignment with Marking Criteria

| Criterion | Status | Implementation |
| --- | --- | --- |
| **Correct node coordinates** | ✅ | Imported directly from `node.py` |
| **Correct element connectivity** | ✅ | Imported directly from `element.py` |
| **Sign convention preserved** | ✅ | No manual flipping; visualization matches raw data |
| **Visual clarity & scaling** | ✅ | Proper axes labels, 1.5x Z-expansion, auto-scaling |
| **MIDAS-style 3D plots** | ✅ | Vertical extrusion + vertical hatching + heat-map colors |

---

## 📦 Files Included

* `xarray_usage.py` – Dataset inspection
* `task1_2d.py` – 2D SFD & BMD
* `task2_3d.py` – 3D MIDAS-style SFD & BMD
* `node.py`, `element.py` – Structural data
* `screening_task.nc` – Force dataset
* `SFD_BMD_Report.pdf` – Documentation

---

## 🏁 Conclusion

This project demonstrates how **professional structural post-processing**—commonly available in commercial tools like MIDAS Civil—can be reproduced using **open-source Python libraries**, while maintaining engineering correctness, geometric fidelity, and visual clarity.

---

## 📜 License

This project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license](https://creativecommons.org/licenses/by-sa/4.0/), as required by FOSSEE for screening task submissions.

---
