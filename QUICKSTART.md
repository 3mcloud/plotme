# Install
* install using [pipx](https://pipx.pypa.io/stable/) from source (recommended if you want system wide availability)

`pipx install git+https://github.com/3mcloud/plotme.git`


# Use
1. navigate to a directory containing tabular data in csv, xls or xlsx format
2. generate plot_info file
```bash
plotme -gt
```
3. edit the plot_info json file e.g.
```json
{
    "title_text": "plot title"
}
```
4. rename the 'must_rename_template_plot_info.json' to somethings else but keep the 'plot_info.json' portion
5. run plotme
```bash
plotme
```
