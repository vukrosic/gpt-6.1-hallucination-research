import pathlib,json,datetime,sys
p=pathlib.Path('.');x=next(x for x in json.loads((p/'lanes/1/SCHEDULE.json').read_text()) if x['run_id']==sys.argv[1]);a=p/'runs'/x['run_id']/'attempts/a1';a.mkdir(parents=True,exist_ok=True);(a/'dispatch-actual.json').write_text(json.dumps(dict(x,dispatch_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),attempt=1),indent=2)+'\n')
