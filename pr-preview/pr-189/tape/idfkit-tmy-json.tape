Set WindowBar Colorful
Set FontSize 16
Set Width 1100
Set Height 420
Set Padding 20
Output idfkit_tmy_json.gif

Type "idfkit tmy 'london heathrow' --first --json | jq '.[0] | {display_name, dataset_variant, wmo: .station.wmo, url: .station.url}'"
Enter
Sleep 3s
