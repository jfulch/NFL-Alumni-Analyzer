# NFL Alumni Analyzer

### Python version:

- `3.11.3`

### List of major dependencies:

See the full list in my [requirements.txt](requirements.txt) file.

```
beautifulsoup4==4.12.3
matplotlib==3.9.3
pandas==2.2.3
plotly==5.24.1
Requests==2.32.3
seaborn==0.13.2
selenium==4.27.1
thefuzz==0.22.1
```

### Links to my data:
- [Raw Data](data/raw)
- [Processed Data](data/processed)
- [Test Data](data/testing)
- [Final Data](data/final)

### Links to my results:
- [PNG Plots & Charts (pie chart, bar chart & heat map)](results/images/)
- Interactive Plotly Scatter Charts
    - [Raw HTML](results/interactive)
    - [Deployed Plotly Charts Home](https://jfulch.github.io/NFL-Alumni-Analyzer/)
        - [Defensive Performance By College](https://jfulch.github.io/NFL-Alumni-Analyzer/Defensive_performance_by_college.html)
        - [Offensive Performance By College](https://jfulch.github.io/NFL-Alumni-Analyzer/Offensive_performance_by_college.html)

### Instructions on how to run code:

1. Clone the repository to your local machine.

2. Install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```

3. Make sure your in the `/src` directory:
```bash
cd src
```

4. Run the following command to execute all 3 python scripts and sub processes with one call:
```bash
python main.py
```
*Note: this process takes ~5 mins to complete, and will update the console with the progress of the code. You can alternativly run the code 1 process at a time by running the following commands in the correct order:*

```bash
python get_data.py
```
```bash
python clean_data.py
```
```bash
python analyze_data.py
```
5. The code will generate the following items:
    - [Folder containing the raw data](data/raw)
    - [Folder containing the processed data](data/processed)
    - [Folder containing the final data](data/final)
    - [Folder containing the test data](data/testing)
    - [A folder containing the results of the analysis](results)
    - [A folder of png images for some of the plots](/results/images/)
    - [A folder of interactive plotly charts](/results/interactive/)
