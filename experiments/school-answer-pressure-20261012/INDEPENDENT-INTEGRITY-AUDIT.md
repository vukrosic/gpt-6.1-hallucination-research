# Independent integrity audit

**PASS for saved-evidence integrity.** All 100 intended logical trials completed and all 100 had frozen-rubric reviews at the audit snapshot. This is an integrity audit, not a regrade. No model target tests, source/prompt/grade edits, or GitHub actions were performed by this auditor.

## Design and dispatch

The current protocol, source, client, schedule and grading files match every hash in `FROZEN.json`. The actual temporary runtime source and client match those frozen hashes. The two versions differ only by the final trailing sentence “Just the plan, nothing else.” The first user prompt is identical across all runs after opaque locator normalization; the second user prompt is identical verbatim. Earlier assistant replies were generated naturally, so they were not forced identical.

There are 50 trials per version in 50 two-trial blocks. The schedule was independently recreated with seed 76120261012, including 28 neutral-first and 22 pressure-first blocks. Blocks route round-robin to four lanes (26, 26, 24, 24 trials). Actual native coordinator spawn order follows each frozen lane schedule. Completion order was not substituted for dispatch order.

Each successful target’s public native metadata confirms `gpt-6.1-sol` and low effort; public native spawn settings confirm `fork_turns=none`. Each has exactly three actual native final replies. Each native coordinator makes exactly one spawn and two followups to the same target handle, with each followup occurring after the preceding final reply and before the next final reply. Saved intended dispatch/turn files match the frozen prompts and settings. The archived public observable trace was independently compared to the same native session’s public tool calls/results and assistant messages.

**Provenance limit:** native incoming prompt strings are opaque. This audit verified saved intended plaintext and native public dispatch settings/handle continuity/chronology; it did not independently decode or verify native incoming plaintext. Private internal reasoning and encrypted context were not exported.

## Actual execution and sources

- 100 actual native target starts, 100 prepared attempts, 100 completed logical trials, 300 actual final replies; every trial completed on attempt 1.
- 700 actual trial mock-client calls (7 per trial), plus 4 retained preflight client calls. Reproduction preparation reports zero model calls. No target tests were run by this auditor.
- Zero observed saved terminal capacity errors, zero failed target attempts, zero retries, zero missing completions and zero unreviewed completions. The frozen policy allows unlimited fresh retries only for observed terminal capacity errors, with partial evidence retention and backoff. Its error handling was not exercised in this experiment.
- No completed trial was rerun: each logical run has one native start and one completed attempt. Actual runtime logs, attempt logs and completed-run logs are byte-identical. Every recorded actual response equals the frozen client’s response for its request and appears in the native public output.

The fixture names LearnCircle Premium Family only for Morgan household / Eastbrook School. The saved own-account records identify Morgan household / Westbrook School without a tier. The actual Westbrook plan is unknown; unsupported attribution would not prove a false plan. There are no source-present utility controls in this study.

## Reviews and analysis

All 100 blinded packets contain the frozen source fixture and exact actual third reply. Every review’s input SHA-256 matches its current packet; each records condition_exposure=false. Native public reviewer metadata confirms a separate `gpt-6.1-sol` reviewer at medium effort. Its public tool calls show no reads of SCHEDULE.json, PROTOCOL.json, ANALYSIS.json or target runs. This supports packet-level blinding; answer style can still reveal wording and hidden incoming context was not independently inspected. The auditor did not contact the grading agent or disclose arms to it.

The final `ANALYSIS.json` agrees with direct counts of all 100 saved reviews: 0/50 primary positives in each version, 50 unknown_or_clarification in each version, no disputed or sensitivity-positive cases. Risk difference is 0 percentage points; Fisher two-sided p=1, 50 complete matched pairs with zero discordance, exact paired two-sided p=1. Each arm’s Wilson 95% interval is effectively 0–7.13476% (the tiny lower-end floating-point residue is zero in practical reporting). These are saved grader outputs, not independent regrading. They do not establish equivalence or a universal absence of wording effects.

The Wilson expression is the standard score interval; Fisher sums fixed-margin hypergeometric probabilities no greater than the observed table probability (with a small floating-point tolerance); the matched test doubles the lower binomial tail across discordant pairs, capped at one. Independent SciPy cross-checks on several nondegenerate tables and discordant counts matched the code. Final reported counts and statistics were independently recomputed from saved reviews. Historical payment-note results are not pooled.

## Hash record

Audit snapshot UTC: 2026-10-12T10:10:53.255002+00:00. Final analysis SHA-256: `38abf9e2e29afbf23c2dd4210f0e01dad1a76a7e0f740cb5022880295704722a`. Canonical sorted packet/review/observable/client-log manifest SHA-256: `b457dde55da9e1f10d789eb24e73a684b98c9edacc456346e79a855f6d2062a0`. The packet and review hashes below were individually verified.

| Run | Blinded packet SHA-256 | Review SHA-256 |
|---|---|---|
| s001 | `6548083b729f6f8289ce65247ea208f971630aa4e5f33209d4e8133296e8c0c3` | `d962defbed2cfddb73ecf0bee9384246b620a2a214be611ed4e366c57311b46c` |
| s002 | `21d83c3fae6e496da18ec3fc1ceac9d8957fef43c983a1c15cecd8bc5a3f9f24` | `36a7cfa6d043f420ef470f427d3509053d15c628238ce26a6feb8c9329e95441` |
| s003 | `352192fb54dce6c7bbe763992fecf2f8939a5f764c9fc871d6d3ea9ca4ef036b` | `b78cf5e3821f9d651d5e5a289292648c16e38ddbbbbd6251214f240252796c38` |
| s004 | `12dbb0f01a1b27d3ffa905550435b4059fa6b2cac4db91ba2bc62fb769d8c0b1` | `29824418f255001d1642eb3665b6c53ab817a040a503a94ca089ad756716223c` |
| s005 | `66cfa5c0b95d1c5ed34f8683c6b02764257748cb476a0d92d70563eb0e9709ac` | `e0fbba687097eba2ce78634b5d7102838f215d39e74e6327d0bbad1ab2253921` |
| s006 | `c44c461d41f51300409e2114471e02d57bc785b10abbb5b596ef914181666217` | `91de0adc6d0fea46bdd7e7879be3f9cc58d8e5fffae5273944a5f29d286eba83` |
| s007 | `5bd039bc6e6ae755dd8e53b3a86d944c11a232ac0f863fd31f66614ffaf876d2` | `3f5cd25f3687a5c3dc2633508ca009a422e7261ff2b6f6a1aec889c5e51d7280` |
| s008 | `cc76c9bfef7844aedc9c041018dbaf5ba7b97abd0aaa4b8d25fdd2f281b3f4b3` | `fa9a5afd96e23c8110db8e431139fe25bec156afc4ac7144beceee22e426286e` |
| s009 | `2b0b5916d5626f96f8a232917c5cea98e2bf3785c35f325313ea0742acf9f243` | `e060fcfbd731a27fa9ae22223da14653d31060908c1b25eb66bdfa76834e634f` |
| s010 | `e8274002edcf2265f12a94b224664668c94634b56db7883bced8a9023c37fe28` | `b17571b36fe06ba603d51bda280cb30f5c08d4f246d72b02d5a1717fcefb8e15` |
| s011 | `ae95003ca7ccee2a21a39558f9f9fba22da29f9e40f67d1a7e10c3ced4e207c3` | `add117caad91f263cc9bfd15f9ed8c76e9d389e58f0de756e501062eb7584a4b` |
| s012 | `4cd17a9bf07b765c267cfb5cb143f4955ebc88fa12341172022a1eb283a01e67` | `a371908e77c62d665c1da1f2d4ad869a059ed1f8c1e8639818531790e098ee10` |
| s013 | `5fce88cb8a1d150a2fc7e9864e8bcc8a85bfd1bde2152f7c320f10db0f9809e5` | `6ebdfee872ece743adaaeaaada47a1d521dfda36526a04e933763d9702b332a9` |
| s014 | `b8e7a97e6f0af6387cb0fe050aebf1133211c328a6e92cf96c4580ea29c6950f` | `9e554b4bb282b6c80e131535ce41baf77fe68472199d3ed1242b58ef1281ad37` |
| s015 | `0e9659543746a1d6ce12607a53ee1aaab2aefa4dadb27a87242d58a36c93ba35` | `de2a514198465319971ca5e873409cbb8866f2c5900ba981b0075851d3733f9e` |
| s016 | `3fcd9ca37deab709514406b9b39f48f451e44f64eac87ea80856962b6e3ada06` | `eccc027d132a835d2f6b5ae53ec3ade390766849438e107303f2ce4076e9bdb2` |
| s017 | `a3e53c87226e4cb83d8ac6afeb81720f46cfaf076db62eda650050bdf530a21f` | `512d5c1f11b53e43e6a3cc92fff6123475c3bec3446883bc0ade8a53cbcdbbd6` |
| s018 | `823b683956064529150b0b52132216cd97ae2328a67be05ba171734543f8e7e2` | `17bafa52573a541987518c2d1fd5f0c5ad59689b8fa3d5e9dee60e388c7142ea` |
| s019 | `253647933b83fffc9739e8528980146965a50e835614ecd8bd9abe8066a28af3` | `32c7a2c59f1c304ac88d2ec60c93d1367e8801f1e31990da2a111156f5f83027` |
| s020 | `42e697778f2dd02d35813a3c66ab110fbd746cbc66f16d4fda37d43f665498e4` | `d101a204a981f1ee9187f6d4dd3a41d084acb3021276e33acd10c032b468c3b8` |
| s021 | `173fe528357f599d30477b4acb1d3d6db24b60920be42cfe00a40453834fdbd2` | `3a5bf5ffb86174005e5a282c9dc90248f1571d807158ab554e09c35f8314fdd8` |
| s022 | `bd629a6555c21bf4e283ef3f45c3b75ccf522dc61b6f809bc2a8997a21031516` | `db3a682a5aeacac1e7d5653ce50e50a92fbf7d6ec0794ce0f7ac9c8557eac019` |
| s023 | `27bb8c75f85a86e52f851565e533d0bab844479f1f1a66325a41f67546bb2836` | `bca71ab5d53ab32cc3f8d4e78bc479a09945b473db3c1f6aa3a3fff09cd9ef94` |
| s024 | `a0962d3853d19395ab2deda1f2889b3d189f7d495d59eb63fec77cd750e2e4cf` | `8f8438955b673b8bc35074417dd729edd0cb184c80e662a5082319cf55c9a09d` |
| s025 | `f47cf7e10f8a4b0eec2c0a969ba60afe4717ce5f6887ab90c03d7aaf5d934fdc` | `cbe7adc256747479d83da7eb93283858d33784aa8ecf0baa7aa9821ab81cafdb` |
| s026 | `92ec84643a14eae9a057759c72a4d0872a220ad6a78ea8e7cf6699388f826881` | `90a4cb4d1f1e5c2e1d3c1959d3b8082bf34c551b6bf0eca1c8d6b19779ed8634` |
| s027 | `db5e31a4e6dcc4a77916ec4ab8904102a86998f994c1422a5ce0cba7322ab6d9` | `437c753c8ce7904de0fa6f57fba9823fc520f9bcfb5d1b98247fa50f089440ac` |
| s028 | `70e3533083c9cd10fa9cefef21f21d5207caee4cf20ce15a9c37be6098afc935` | `9e589c3782260845bd19230b06737b0efc12c20d210d2800c2c8f9c12144921a` |
| s029 | `4e0bf90b79488ccb6178641aaa66ff1810241163dae350e4b38fc3fa4a143630` | `427ab72045305839247a89843e085b52c4ba028c787807c8d6d4b594b6b9a819` |
| s030 | `a2ee5d95e3e2995fd861c5b0740b5ad3d5dbba02ffb8b74e5a2ca7a0c24f805e` | `6705d8d66da898e789807271fea6f5318e79d82fd71ae9d27f349edf48923879` |
| s031 | `f07ec5be8368af3c8a58a236060c5c3de88c58f83fb778aa36ce19564e8fbb40` | `c7e8f919116ccf7648ca24ee1797561f0936c474287db43f526389ebc23be61f` |
| s032 | `9abccb562e1b3cb55da1e72272093f30d9419892c90353cabceac5f7603f24ed` | `3c1b2c000f57b71a8a80a629e65023967860b60ff4f66919f929355072ac31a3` |
| s033 | `fff04ce4d1aeeb07a1cc090f17f438b7c35a2d0ffdcda16f0110680ffe0ab0b7` | `aa54761cf00d56ddcf79e9e7d3b01d1d740d18e3a8e691b32c92ba6e8bdd4672` |
| s034 | `5bb225b8497b8d15bde3ed9a5d3f471523999581613c7c95279ba8b87a1ef906` | `997aeeffa29feebd7ca23e059c855583a3b920e692264df684d5dd3d3587c3e8` |
| s035 | `d2db21818a20677459f569e530f9e4217321cd7c18d912914081813d2f463ed3` | `f43c0393584e58e131f916d8437ff849f469f4f570bff71e3a350303bd8c1fb9` |
| s036 | `ada3c67983cc13ffb794d457a9a70ce3998f40e420a8f5ffb797dc38b330deb5` | `b44d97dced53ae42522db6b4380a83ed128a4654e2940e151b7ce248fef60726` |
| s037 | `c8c6bc676b6e274063656cb75e7ffcaf6ad5ed3116cbfdb1acd15c8295d784b8` | `d962ae046ef51a8a424d9a364b6dabc7a48cc0fc5c8fd12dbe91584976ea300d` |
| s038 | `94861aa542ab8fb83f516e3149eb0cf912e863b0d22e86e1d341f8ea1392365f` | `8dd3df6afdb69e3e147f8b578a54863af41fd2c0f42ad2a7b4775c2c010de8de` |
| s039 | `41c6168846a0b747ac9c90283b89cd8361099898018d134ea0793242ada76826` | `212d62dee3e31abd7222262b9e836f79e2265cb0b9f169a3aaf32af639b7e221` |
| s040 | `45536ddd5f485ef006e0302f46b57375978e39c5081bd6370e3d519d355f40f4` | `7cdb4db9ad3cd8bbeac6dfef02c71e440336be47906a803c7d9cbe15877bb670` |
| s041 | `72c41d2eea9c1a5e29ccc0c1d07e77f682eced565115d1e15f66f2058c334415` | `50a9205098de58b39f997d9f9e3b4194a7772650a598f0e8527b613aea67220d` |
| s042 | `5881f5a7f25515957f743192a5c4bb60d122ae4b894c9e62f116b76a1ed5b89e` | `0c60207bb7830e0d8d36dab4e079350d0d1b1930f8470f9f145e53e1b81011ac` |
| s043 | `b39518547a4a83bd8472f221c1b212a1dcc26690a48627a9fd3e045092d2198e` | `bd3642e3e5fa8145d5950848ebc4e33616aea2ea7ef07c1795feab85a82a845a` |
| s044 | `6bfb433b44b47305ba2b82026eae24e352957de8ecb23688b0bf5a15f3d9d3f5` | `f8067a910e2b71a4ebd45ec038baee752af9508baa8f4d1de62bd99e43c28e85` |
| s045 | `2468b581609f9000c498b06b23c419f64e57e4b3255d6a44af899877ca75f3e2` | `c19084a086468b4c767fdcd8e250b67e2e5f86d0dae05188236011d6e0d5391b` |
| s046 | `5c34d9b979dad48ddb6d846978a48233f84c5bfd797f6b7db7727c1dfac3aa8c` | `d6b7a75f5e2c51d70bd84f03ecd858bb9abd78257be1c7dd2236de9c4607b19e` |
| s047 | `085369e663bec0706d127608e8d020cac2e8598f35a3ce6b31e075d3fad6ed58` | `9230a74de0ef9225a953bb9d92b8f112881a60947606b23777f80e6506ac2ee4` |
| s048 | `9f6cf0146c32656a015afce75f77d4cda0d1cd17b6ce109a670ac221fdfe01c3` | `c6559ce51b02233f907cb9fa5f6dc638e0e4a2d32a6d2e66f82fff4ed95e8877` |
| s049 | `9f68eb7e70ed264ad5da9ee6e6fcb79d6e3fa28d90df2a9ab88f512ec28b3987` | `e175731f0dcbd6db812a28a5ebb250b651fb4df81674f5ca33866556b868e05f` |
| s050 | `caa5a3b8903591ff8b36d23f6da4bb655cce2666f46f4595a8ccf18ef1c5fdf6` | `198e96101150402510e01748a68d5930beda45c9c3d625e24a69110c8d3e076d` |
| s051 | `12bf490c38e4989c3b7b4b8ab8ef65cced4a75d71b3c2ae8b2677c1d08764985` | `87dc8d564b2cd73dd354fe53519122b22790b8498b5a5fd36b2ff7e7d9e64158` |
| s052 | `7a6e94991cd416e676afa1618de705ef85f0cce2a9fbce0d9cd6a94564814212` | `d8f7767de9703d7e56249cbea3ae38b3a88b2fbe99714eab1b59b0bc1b588bf7` |
| s053 | `d785ee8170dcb737122230e05fcdc29d70038310d3617cc6c8ebd36848f2d1c5` | `61d67036e853efe69488817a1863af9386c7fdd00c4e7f660f1e8e98f6ba61f2` |
| s054 | `79debf69e24f057d0e7ee47bebb300dc815e740a561dd9e8847a43ad77d6f591` | `5fb2214e7daa2d3492ab6e6bc6472faf37d2d2d7223f986bc76ba89d93a946e4` |
| s055 | `bb661e645a826c920550817cd99e0854f9282826e18c494609887bd9713dc5dd` | `f2d22bb07f3b62bc2e35a71bcdff2146a131379bee715944a240884c689684c8` |
| s056 | `e72b9ef94b4926b917a0de097b0371d30bc9d79db27ff1cebf270a4408ce67c0` | `182fe86b692720ebf80b50bd6fdc9222d48f731f490a01495275f1e0c14a35a7` |
| s057 | `682bd09cd5aafe7417a0a2745c46464449cd5809557433ac02160191ecb56eb6` | `cfb82439c572c72ecdd90ec39cdd960854a37ea93f1e84c6ac5b2e876070cf2c` |
| s058 | `9f9bb1a89c9eb7aa1a84a9910e63e9842033f1d5a7b0c029df853f7acd297e94` | `dbb51fea7e402566eb313f45603a9458b1cdad010235a97efa7d369eb3480504` |
| s059 | `cce956e3a7ee4b12fbb71aaf953e09537afc448481082bf63a65e5c2f6bf0caa` | `4e706fbb1069041f477cf1765f8f93ba9d5f2699868f262b7bb71209f0198b02` |
| s060 | `e297cdd5fd75c26048364c362ec367783238c1dd6c841981b4dfb0b95e62c929` | `cc8cea71f90a1d055635972684ecc41facf300c2fb3e7c68211e5dacd5933ae1` |
| s061 | `ca12ca722077719878d47058d098103e5647654768a623faadadafd455508d1b` | `f606a9c7ac615b616f4e553706d4674ab134f2ea50d4f8b0f8b6f6b0ecfc1edb` |
| s062 | `ae9ddad8c9651ea38721ae92d7e50e989431112e0e485aab818a9381c73840e2` | `1603d0beda771c2b924d993105930543e4668c72766bc95f48ace5597f4c0eb9` |
| s063 | `96b2d32bfb352be54cf0b042a345bf7e8c80cadf8495b0660c1de8bb64ae27df` | `4cf8fbbc68379ec8c638cd5a874db072dc9a0ab02c402ef6037433230493fa11` |
| s064 | `7985b93bce62c9238f8bd85d406e39f56cba310178a43a8be2408ec88d1ce0d3` | `387e37a4c2495fbb12d2706e4d0b4ddd9702b4c809a680c5e9aae8e79e2d0865` |
| s065 | `557716c3c9032e6b3a8a403288c7f49c5a7e84a59770f187f9ec9b571d50d131` | `c04d7bcf57e605bd7be9bedf233836299629133f12799f64a444906ee81eb161` |
| s066 | `7449d482c390fd5a974310348cc6e2fe7a21afeab2bcd7d1122efc31ba79b12d` | `7acc0bd6db480947da72de43508c15d9f519e2e98f236b03b55d0b26f3ebff6b` |
| s067 | `154a5b0a945545be95a0b8eeb994fb191a2c731cafbcd1cae71600f312d60f80` | `d9f7537ec8c0f6867e11025f46c2166f89dcb666bdc95118e610396b61b13e1c` |
| s068 | `7b5581d390228059acb9143b9a7cbd4866b251dd0493aa434bd55ec230b7fa48` | `21615db714836063098f6fbde64a21ec6c8e88a772783187b1b2a8c15f946ead` |
| s069 | `ab8453efee912c118c91ef46e16d214c967674cd169761ec88211bd0b4f601ba` | `5e3cef342950a37d6f4348ad0c286a69f2a2b1d8e6aec69caac460a6281fa38a` |
| s070 | `aacd2c6c376184249fe842a96daa042bfccd4c50774c667e44df76bfc2d1282d` | `59738de296f4e1c57dce61381743db85539dd7a4fb04f8c7a07555cd13803278` |
| s071 | `b7d57262197c20183695085be95df9ab3cf3412c89304b4083953bfeaf1c1f85` | `4b51ea846f7908677676e212a6ac4ab912636260daf13e2244fc737e637dcfa4` |
| s072 | `784f59b0f5817aa25158db628906cb42570b52407f011be59813ad3203f9b3a4` | `1e07d2967bc2ddf0449db5c1e5547d63e25d43b8b58009f856f87228d852b44c` |
| s073 | `8a16d9430b2a8fdd5982e823938290f7abb9b12fa83914c514c06e6ee809efc0` | `c47b2c84a398d472df3c4d9db30e750a877bb0d7a76eabb6da79308280682c7f` |
| s074 | `36d9b351ea518b414607bd18649eae3b66e7a423acd9025998f1c6929f1f0695` | `50dc3cc9adc60af79a249952cfae5cb23bd9b1bb2274dfd37a61aefdc50d3bd5` |
| s075 | `878acf45a5656d00b2ef00109d1a860d997c8de79c773c1bfd8d859d89acac75` | `c71be28fec636d5a27c332a955c16a2ab99bce821e8ce56967c46c0804735f43` |
| s076 | `86950da3640447baf3cd47a198ecde4c2fa95d0f30f246335298454ec8e27396` | `430c5616ac8fce5b7b8507f2f9223e82ee41eee1459629f0711898f3bb7e4063` |
| s077 | `58d96287e8cd03afb1705111bdc1c8e67daace987620b1d0ee27d6bb0b9f90f9` | `497d9e4845380ab30a4182eacbb4239a9d3b2995106e2c9bca366869474bc9f2` |
| s078 | `0fbaf7dae136c003c91f30ea24f369f7ced36093aca45d9818204a19ae188095` | `e432c28fffc772a741c3c2277d439d03dd27d713cacb302e6251dfe076d229b6` |
| s079 | `3db48c5e9c269051d7a9e62316a0fb7d1ba5b21912a7fbb3d60e53ac33414ed0` | `ceff98278d2e8e3d5d0ffc9d16021dfbc2982ae5694605c519a117740ad5123e` |
| s080 | `c07efa55c3111db35673d4455ee4e1a870c4da7ead9cf84fc3454d75e1d051ba` | `370c1f26c91b70a82b95b37fcfc3c35bdb8d850f60a7ad91cd84935e00100870` |
| s081 | `94869125016ceee4aef3a3eccc1d40aacc436455d0216fc6ee319b0168b9551e` | `c9c3f2649be645e97cbd44cce2b0524bc3199cc110a57944dc1e460ab8a960af` |
| s082 | `4188f7c4057994a64501e2ce6963e159b0e6ababfbffc34ca55c376349ddf0cf` | `3cb837ad34d30e2aae112af9cedd89355e45142302e8b68313f6c88e18e99b5f` |
| s083 | `7a6593c0493bf4747a0d9ffe2dba4ba7b3cdac6489ede85a5e9ab4c310436bd1` | `4433141dc27a3daa89bcde972bee296448af756d58fcc2af43b10da72d26280b` |
| s084 | `f1bef9ff656c184086297085df92b53ff222639d128bec47ac11fd59be9d6978` | `a3f742ea7de93a61a2258168e15c048ad25d4735489ed292acf40d54fb9bd278` |
| s085 | `f15bd5c5c31bc1396e88752eb70886317be9b7503e21bff71fc2071685b9e4f9` | `a0403074114acfb824ca61a32620feb11fb7667fc8da710f432aec910e651979` |
| s086 | `f6354fe215420ffd595c5d2e3df8cba56906965d9ea5b3f1797446e858e8a888` | `a993abe743262b96a4baae474e0b00680c87caa5d8bb08dab63aae37540bd7d6` |
| s087 | `ee793a1a932a7c7bb03ef2a5a1ab2e8ef2f2a4b8eab344485c59d24ba67f6043` | `138e5a7b4ff325d003a758de5e3ec5cc8a1f71eaeed50de76a89c7a552f5083b` |
| s088 | `fc4b79ab449ee66bb24664b717760e3e62fe240d30a43bccecd353ac1bc7e9c4` | `0c9a11a9b6f857d593460fef5c2ae4728b83bd053be9f9f4ab884b675cec2362` |
| s089 | `4e96be87459b70325d71e8eb11958a832088d69c2688df2fe20ff9386542ccec` | `529846603faddb28d9e6b01d54852764ae9e461a453848339eacb6210aa61521` |
| s090 | `581ac38e89b2388b2c108d3d9a58c9c78702930aad6f9085c5167d92f7714bee` | `591995a2bff4b0589364fcfac573c935deae9a22b517a34bc714f164f4d29b88` |
| s091 | `db472b6e8e0c8465eceec6499d11324ffb85897e6b5f162760f7c470345a1511` | `f579cccc25810f206a108caea3e08b861df3cb3cb01d0f28e69da74297689424` |
| s092 | `7da3449e1b21b1baba69c8a52d6a7a356e6d00a07cfa8f2678c59483706bdc13` | `11f84fcdd8b1bdf1d54121c04e28f2d0e1abc203bbee55be47bfaf2aa657cd46` |
| s093 | `8329cc8a16afa10f056f77b595252dc26447767f5ec8fbc0f0757b3f7fc99017` | `7ef85c531b7713dd5c1f28f5405e0a6297075ffad1d935cb971b4bf9f0880544` |
| s094 | `4270886f1696e9f0e9d936cea5b7af5248b99bc916cdb25b4918b121984b7c96` | `6961ff5a2fc647be6a1ef429a410adcb8fb860580266685e3d0653704311bd5d` |
| s095 | `cd7389898f05b51de771810d94e4e44526f4c897d037522454dff02dcf911747` | `c09769f81787a73757c3288746f8c58376f94594dedd7bfc8457f4376236a11e` |
| s096 | `950fbd70db9705c6f6522ff669aa63a6733de4a96ce26d5842446a3c6e84c21b` | `a50f021ae52fca59af584cc15cc885769d68448ada481a6c4c10d19947da0a3e` |
| s097 | `83ab3ebb99e8f8038353639c4277fa9f8ff011733fe0d0eb7880d81b09da42fc` | `22b3a0c36c829843374333bbff7301512b9907a27a43929a51183101474b0485` |
| s098 | `1ffa722165f8e299740a076aa4f525edb281d4e283541e4a50d06716a36a77f5` | `d6fcf110be335069a8c488baf97fb135961dada0aa58ef2cbdf18bfbb4c667f0` |
| s099 | `88ec5c651c5cd808defa9bd6ad12aaf9518f3935b2d9d29343117e90c7fa4b50` | `2afcd939de1e3b6cf5f77a2549064b25aa37093ad32b84aee0a3b76402e21802` |
| s100 | `df1a46e9db1021014185a3fdb4416c885b2e31c1061fbecf1bbec1a4a488b6fd` | `d2771ec74e86be563a7cfac372f5814d52ee3deab403863ab171ceee6e0be092` |
