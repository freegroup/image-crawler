import matplotlib
gui_env = ['GTKAgg','Qt4Agg','WXAgg','TKAgg']
for gui in gui_env:
    try:
        print("testing", gui)
        matplotlib.use(gui,warn=False, force=True)
        from matplotlib import pyplot as plt
        break
    except:
        continue

print("Using:",matplotlib.get_backend())

