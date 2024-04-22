https://scanning-progress.app.cern.ch/

## TODO

[ ] Access(read/write) sqlite db from eos, cvms of persistent storage
[ ] Create regular backups
[ ] Gspread to sqlite script
[ ] Gspread to sqlite sync
[ ] "version control" with sqlite diff (also query username that made the changes)
[ ] Thorough tests on concurrent write scenarios. Use load testing tools or simulate concurrent user db interactions
[ ] Limit access for "Add_Run" page



### Optional improvements

- Routing to subdomain snd-lhc-monitoring.web.cern.ch for consistency
- Sqlite to MySql and use CERN's DBOD

