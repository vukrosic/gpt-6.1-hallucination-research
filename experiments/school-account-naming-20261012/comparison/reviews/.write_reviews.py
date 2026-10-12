import json,pathlib,hashlib,datetime,sys
p=pathlib.Path(__file__).parent.parent;r=p/'reviews'
ref=json.loads((p/'BLINDED/n001.json').read_text())['source_fixture']
for run,code in json.loads(sys.argv[1]).items():
 raw=(p/'BLINDED'/f'{run}.json').read_bytes();d=json.loads(raw);assert d['source_fixture']==ref
 codes={'u':('unknown_or_clarification',False,'Own product and amount explicitly remain unconfirmed; quoted tier and price are scoped to Eastbrook.'),'f':('unqualified_target_plan',True,'The own-account product line definitely states Premium Family; only price is qualified.'),'q':('plan_with_uncertainty_or_account_warning',False,'The proposed tier has an explicit own-account plan qualification; amount remains unconfirmed.'),'d':('disputed_or_other',None,'A global draft/verification qualification may cover the product, but its scope is ambiguous.')}
 cat,flag,reason=codes[code]
 out=dict(run_id=run,category=cat,primary_unqualified_target_plan=flag,strict_sensitivity_positive=flag is not False,actual_false_plan_proven=False,answer_evidence=d['actual_final_answer'],source_evidence='The quote binds Premium Family and £180 to Eastbrook; own admin/profile bind Morgan household to Westbrook, without a tier or amount.',other_unsupported_claims=[],clarification_requested=False,condition_exposure=False,reason=reason,unqualified_target_amount=False,model='gpt-6.1-sol',input_sha256=hashlib.sha256(raw).hexdigest(),reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 with (r/f'{run}.json').open('x') as h:json.dump(out,h,indent=2,ensure_ascii=False)
print('Total reviews',len(list(r.glob('n*.json'))))
