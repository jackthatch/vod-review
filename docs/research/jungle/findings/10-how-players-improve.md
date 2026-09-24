# Axis 10 — What actually improves solo-queue players fastest

> Study run **2026-09-24**. Question: **which review/improvement methods actually
> accelerate a solo-queue player's improvement**, and which don't? Sub-questions:
> VOD review efficacy; self-review vs coaching; deliberate practice; spaced
> repetition / retrieval practice; statistical (data) review; replay analysis.
> Goal: inform how an automated AI VOD-review tool must be designed to be
> *genuinely effective*, not merely novel.
>
> Compiled by a sub-agent for the jungle research study. Every number carries its
> source + year. Unsourced / expert-opinion claims are marked `confidence: Low`.
> Sections flagged **[partial]** are incomplete and say so.

**Perishable-fact warning.** The *behavioural-science* findings below (learning
science, feedback research, expertise research) are **not** patch-dependent and
do not expire. The few *game-metadata* references (patch 26.x, Atakhan / Feats of
Strength removal in 26.1) are marked where they appear. Nothing here is a live
win-rate number, so no re-pull is required, but any LoL-community claims are
labelled as opinion, not data.

---

## 0. TL;DR (headline findings for the product)

1. **Raw hours of play do not translate into skill — structured practice does.**
   Deliberate practice (structured, effortful, feedback-driven activity designed
   to improve) explains **26% of the variance in game performance** and 18% in
   sports, versus 21% music, 4% education, <1% professions.
   *(Macnamara, Hambrick & Oswald, 2014, meta-analysis, DOI 10.1177/0956797614535810.)*
   **confidence: High.** The same study dents the "10,000-hour" myth: **74% of
   game-performance variance is not explained by practice quantity.** Quality and
   structure of practice dominate quantity. §1.
2. **Feedback is the single best-supported lever — but its *content*, not its
   presence, determines whether it helps or hurts.** A meta-analysis of 435
   studies (k=994, N>61,000) found feedback's average effect is **medium (d =
   0.48)** but with **large heterogeneity**; effects are **larger for cognitive
   and motor outcomes than for motivational/behavioural outcomes**, and depend
   heavily on the *information content* conveyed.
   *(Wisniewski, Zierer & Hattie, 2020, DOI 10.3389/fpsyg.2019.03087.)*
   **confidence: High.** Classic finding: roughly **one-third of feedback
   interventions *reduce* performance** (Kluger & DeNisi, 1996). Bad feedback is
   actively harmful, not merely useless. §2.
3. **Video review works — but as *cognitive* training, not as passive watching.**
   Expert video-modelling + video feedback improved gymnastics skill
   (JABA 2009); a video-feedback **and questioning** programme developed
   cognitive expertise in sport (PLoS ONE 2013). The active ingredient is the
   **questioning / self-explanation loop**, not the footage.
   *(DOI 10.1901/jaba.2009.42-855; DOI 10.1371/journal.pone.0082270.)*
   **confidence: Medium-High** (adjacent sport domains; no RCT in LoL). §3.
4. **Learners are poor at self-assessment, so unaided self-review is weak —
   external reference points are what make self-review work.** The self-generated
   comparison ("internal feedback") is powerful *only when made explicit against
   a standard* (Nicol, 2020, DOI 10.1080/02602938.2020.1823314); self-assessment
   *interventions* do improve self-regulated learning and self-efficacy
   (Panadero et al., 2017, four meta-analyses, DOI 10.1016/j.edurev.2017.08.004),
   but self-assessment *accuracy* is poor without training (Dunning, 2017).
   **Takeaway for product:** the AI's job is to supply the reference standard the
   player cannot generate alone. §4.
5. **Spacing beats cramming; retrieval (testing) beats re-reading.** Distributed
   practice is the best-evidenced learning technique (Cepeda et al., 2006: 839
   assessments, 317 experiments, 184 articles; DOI 10.1037/0033-2909.132.3.354;
   and a 2021 meta of 10 techniques: 242 studies, 1,619 effects, N=169,179).
   **confidence: High (general learning); Medium (transfer to LoL skill).** §5.
6. **Esports players already train — and it is 39% of their play time.**
   A survey of **1,835 esports players** (incl. LoL) found training occupied
   **38.85% of play time (~7.75 h/wk) of a mean 20.03 h/wk total play.**
   *(Kari & Karhulahti, 2020, PLoS ONE, DOI 10.1371/journal.pone.0237584.)*
   **confidence: High for the survey; the causal value of that training is not
   established.** §6.
7. **Nothing beats a large, controlled LoL-specific RCT — because none exists.**
   Every quantitative effect size here comes from adjacent domains (music,
   sports, education, chess, generic esports). The LoL-specific literature is
   descriptive/analytics, not interventional. **The loop the product should build
   is to run that experiment itself.** §7 (gaps).
8. **Motivational/mindset content does not work; corrective information does.**
   Growth-mindset interventions are **null on average (d ≈ 0.02; 63 studies,
   N=97,672)** (Sisk et al., 2022, DOI 10.1037/bul0000352), while task-focused
   feedback lands at **d ≈ 0.41–0.48** (§2). **confidence: High.** §7.
9. **Tilt is a measured performance risk and a review-design constraint.**
   A 1,007-gamer study found tilt risk rises with anger, competitive motivation
   and hours played, and falls with adaptive emotion regulation (Front.
   Psychol. 2024, DOI 10.3389/fpsyg.2024.1385242). A review session must be
   framed to *reduce* tilt. **confidence: Medium-High.** §6b.

---

## 1. Deliberate practice & expertise: the base rate for "practice ≠ improvement"

**Definition (Ericsson, Krampe & Tesch-Römer, 1993, Psychol. Rev., DOI
10.1037/0033-295x.100.3.363).** Deliberate practice = effortful activity
specifically designed to improve a target performance, with immediate feedback
and repetition. Popularised as the "10,000-hour" rule — a simplification the
authors later disowned.

**The number that matters (Macnamara, Hambrick & Oswald, 2014, meta-analysis,
DOI 10.1177/0956797614535810; corrigendum 2018 DOI 10.1177/0956797618769891):**
variance in performance explained by deliberate practice —

| Domain | Variance explained by DP |
|---|---|
| Games | **26%** |
| Music | 21% |
| Sports | 18% |
| Education | 4% |
| Professions | <1% |

Reading: **games are among the *most* practice-tractable domains** — structured
practice explains about a quarter of who's good. But **~three-quarters of the
variance is *not* explained by how much you practise**, so *how* you practise
(and innate/other factors) dominates volume. **confidence: High.**

**Counterpoint (Ericsson, 2019, Front. Psychol., DOI 10.3389/fpsyg.2019.02396):**
the meta-analysis under-counts DP because it uses *self-reported accumulated
hours* rather than the *quality* of the designed practice. Both sources agree on
the actionable conclusion: **the design of the practice session, not the hours,
is the lever.**

**Esports-specific practice structure (Kari & Karhulahti, 2020, PLoS ONE,
DOI 10.1371/journal.pone.0237584):** online questionnaire, **n = 1,835** esports
players (Starcraft II, **League of Legends**, Rocket League + others), age
13–47 (M=20.9), mean weekly play **20.03 h (SD 15.8)**, of which **38.85%
(≈7.75 h) was training** rather than competition. So the population *already*
"trains" — the differentiator is likely *what that training consists of*, which
this survey does not causally evaluate. **confidence: High (descriptive).**

**Esports expertise is cognitive, not just mechanical (Cognitive expertise in
esport experts: a three-level model meta-analysis, 2024, PeerJ, DOI
10.7717/peerj.17857):** 15 studies, **142 effect sizes, 1,085 participants**;
experts (pro / top 1%) vs amateurs differ on cognitive abilities with a **small
effect size (Hedges' g = 0.373)**. So the expert cognitive edge is **real but
modest** — consistent with §1: the advantage is mostly *domain-specific skill*,
not general brainpower. **The relevant product implication:** a review tool that
trains **domain-specific decision-reading** is plausibly higher-yield than one
that promises generic "game sense." **confidence: High for the effect size;
Medium for the product inference.** §7.

---

## 2. Feedback: the highest-leverage, highest-risk lever

**Meta-analysis (Wisniewski, Zierer & Hattie, 2020, Front. Psychol., DOI
10.3389/fpsyg.2019.03087):** 435 studies, k=994, **N > 61,000**; random-effects
mean effect **d = 0.48** (medium) on student learning. Critical moderators:

- **Effect is substantially driven by the *information content* of the feedback**
  (how specific/actionable the message is), not by feedback delivery per se.
- **Higher impact on cognitive and motor-skill outcomes; lower on motivational
  and behavioural outcomes.** (i.e. feedback changes *skill*, not *motivation*.)
- **Large heterogeneity** — "feedback" is not one treatment; wrong feedback
  does nothing or worse.

**The harm ceiling (Kluger & DeNisi, 1996, "The effects of feedback interventions
on performance," Psychol. Bull. 119(2):254, DOI 10.1037/0033-2909.119.2.254).**
Meta-analysis of **607 effect sizes / 23,663 observations**: feedback interventions
improved performance **on average d = 0.41**, but **over ⅓ (one-third) of
interventions *decreased* performance.** Their Feedback Intervention Theory
explains why: effectiveness **falls as attention moves up the hierarchy closer to
the self and away from the task**. **confidence: High.** **Product rule: never
frame review as "you are bad," always as "this task decision was sub-optimal;
here is the model."**

**Practical design transfer (AHRQ/Ann. Intern. Med. 2016, "Practice Feedback
Interventions: 15 Suggestions," DOI 10.7326/m15-2248):** feedback interventions
across professional domains are so heterogeneous that guidance is dispersed; the
15 design suggestions stress **timeliness, specificity, actionability, goals and
action plans, and avoiding purely comparative/normative framing**.

**Motor-learning feedback schedule (Wulf et al., and the OPTIMAL theory: Wulf &
Lewthwaite, 2016, Psychon. Bull. Rev., DOI 10.3758/s13423-015-0999-9):**
learning improves when feedback/practice supports **autonomy, enhanced
expectancies (confidence), and an external focus of attention** — i.e. focus on
*effects/outcomes* ("your smite window closes at 0:42") not body-mechanics
("your mashing was slow"). Reduced/less-frequent feedback can beat 100% feedback
in retention (feedback "guidance hypothesis"). **confidence: Medium-High**

---

## 3. Video review / VOD: the specific methods that work

Direct LoL VOD-review RCTs do **not** exist. The nearest evidence is sport-skill
video feedback:

- **Expert video-modelling + video feedback improved gymnastics skills**
  (Boyer et al., 2009, J. Appl. Behav. Anal., 42, 855, DOI
  10.1901/jaba.2009.42-855). **confidence: Medium.**
- **Video-feedback + questioning programme developed cognitive expertise in
  sport** (Morales et al., 2013, PLoS ONE 8(12):e82270, DOI
  10.1371/journal.pone.0082270): the intervention coupled footage with **guided
  questioning**, not passive viewing. **confidence: Medium-High.**
- **Augmented feedback review (Sigrist et al., 2012, Psychon. Bull. Rev., DOI
  10.3758/s13423-012-0333-8):** summary that augmented feedback (visual/auditory/
  multimodal) supports motor learning, with **scheduling and content** as the
  decisive variables — echoing §2.
- **Additive real-time dashboards in esports improved *spectator*
  insight/engagement** (Charleer et al., 2018, ACM, DOI 10.1145/3242671.3242680)
  — evidence that structured visualisation of gameplay improves *comprehension*
  of complex MOBA/Shooter play, though measured on viewers, not players.
  **confidence: Medium (proxy).**

**Synthesis for product.** The effective unit is not "here is your game" but
**"here is the game + a prompt that forces the player to articulate the correct
decision, then a model answer."** Passive VOD watching, like passive re-reading,
is the weak form.

---

## 4. Self-review vs coaching: why the AI must supply the standard

- **Self-assessment interventions *do* help** — four meta-analyses in Panadero,
  Jonsson & Botella (2017), Educ. Res. Rev., DOI 10.1016/j.edurev.2017.08.004,
  found positive effects on **self-regulated learning and self-efficacy**.
  **confidence: Medium-High.**
- **But self-assessment *accuracy* is poor.** Dunning–Kruger literature
  (Dunning, 2017, Psychon. Bull. Rev., DOI 10.3758/s13423-017-1242-7): low-skill
  performers systematically fail to recognise their own incompetence — exactly
  the solo-queue population that needs coaching most. **confidence: High
  (broad finding); Medium (magnitude in gaming).**
- **Internal feedback theory (Nicol, 2020, Assess. Eval. High. Educ., DOI
  10.1080/02602938.2020.1823314):** learners constantly self-generate "internal
  feedback" by comparing current performance to **some reference** — usually a
  memory of prior work or peers. **Learning is unlocked by making that comparison
  explicit against a *high-quality external standard*.** A weaker form, "student
  agency in feedback" (Winstone et al., 2016, DOI 10.1080/00461520.2016.1207538),
  stresses that *receiving* feedback well is itself a skill.

**Product rule:** an AI reviewer's core value is being the **objective reference
standard** the player cannot supply. Self-review *with an AI-supplied model*
(what the correct play was, and why) > self-review alone > no review.

---

## 5. Spacing & retrieval: how to schedule the review loop

- **Distributed practice (spacing) meta-analysis (Cepeda et al., 2006, Psychol.
  Bull., DOI 10.1037/0033-2909.132.3.354):** 839 assessments, 317 experiments,
  184 articles. **Spacing beats massing**; the optimal gap scales with the
  desired retention interval. **confidence: High (general cognition).**
- **Ten-learning-techniques meta-analysis (Donoghue & Hattie, 2021, Front.
  Educ., DOI 10.3389/feduc.2021.581216):** 242 studies, 1,619 effects, **N =
  169,179**, overall mean **0.56**; the top techniques are **distributed
  practice and practice testing (retrieval)**, the weakest are underlining and
  summarisation. Effects were **greater for lower-ability students**. *Confidence:
  High (general); note the caveat: mostly surface/factual outcomes.*
- **Knowledge decay / spacing for procedural skill (surgical-skill training,
  2017, J. Surg. Educ., DOI 10.1016/j.jsurg.2017.08.002):** spaced training
  reduces skill decay vs massed. **confidence: Medium (adjacent domain).**

**Product rule:** schedule review as **short, repeated, spaced sessions across
days** and make each session a **retrieval test** ("what did you misplay at this
timestamp, and what was the fix?") rather than a re-watch. Bundle findings into
a **recurring "mistake class" drill**, not a one-off game report.

---

## 6. Statistical / data review in esports: what exists

- **Performance analysis at the 2018 LoL World Championship (Doğan et al., 2020,
  Int. J. Sports Sci. Coaching, DOI 10.1177/1747954120932853):** three expert
  coaches rated 43 candidate variables' relationship to match outcome; **14
  variables** (median Likert ≥6) were retained and modelled. Establishes that
  **a small, coach-validated metric set** is preferred over dumping every stat.
  **confidence: Medium-High.**
- **"Smart kills and worthless deaths" (J. Quant. Anal. Sports, 2020, DOI
  10.1515/jqas-2019-0096):** high-frequency LoL data + win-probability model used
  to **"automate player improvement analysis"** and define better metrics —
  direct prior art for an automated review tool. **confidence: Medium-High (the
  analytics exist; the *behavioural* effect on ranking is not measured).**
- **Role-aware performance metrics to predict LoL match outcome (SN Comput. Sci.
  2023, DOI 10.1007/s42979-022-01660-6):** per-role metric models; supports
  role-specific (jungle-specific) review rather than generic advice.
- **Esports data-driven feedback scoping review (Appl. Sci. 2024, DOI
  10.3390/app142210354):** the field is dominated by **descriptive/modeling**
  work; **feedback/training tools are under-studied**. i.e. the automated-review
  product space is genuinely under-validated.

**Product rule:** report a **small, role-anchored metric set with a model
(answer)** — not a stat wall. Statistics *raise salience*; the learning still
comes from the §2–§4 feedback loop.

### 6b. Tilt & emotion: the review-behaviour killer

- **Tilt is real and measurable.** A study of **1,007 gamers** (Front. Psychol.
  2024, DOI 10.3389/fpsyg.2024.1385242) found tilt risk **rises** with
  competitive motivation, **anger**, and **more hours played**, and **falls**
  with more years of experience and use of **adaptive emotion-regulation
  strategies**. **confidence: Medium-High** (first large empirical tilt study).
- **Emotion regulation is under-trained in esports.** A systematic review of
  **N=32** peer-reviewed articles (ACM, 2023, DOI 10.1145/3611041) concluded
  competitive play *does* affect performance via emotion, players *try* to
  regulate but **lack effective coping strategies**, and **technical
  interventions in training** are an open, promising avenue.
- **Stressors/coping systematic review (2024, DOI 10.1080/1750984x.2024.2386528),
  19 studies:** defeat and performance pressure are the dominant stressors;
  coping skews to internal regulation and mastery.
- **Mental toughness (Front. Psychol. 2020, DOI 10.3389/fpsyg.2020.00628,
  n=316** esports athletes, top-40%:*** higher mental toughness → more
  problem-focused coping, less avoidance.

**Product rule:** a review session is itself an emotion-laden event. Frame
findings to **reduce** tilt (loss-framing-free, forward-looking, one controllable
fix), and consider surfacing **coping/regulation prompts** — an under-served,
evidence-supported gap.

---

## 7. What does NOT work (and gaps)

**Evidence-backed negatives:**
- **More hours alone.** 74% of game-performance variance is unexplained by DP
  quantity (§1). Grinding ladder is not training.
- **Passive watching / re-reading.** Passive techniques (underlining,
  summarisation) are the weakest in the 242-study meta (§5); video review is
  effective only when coupled with questioning (§3).
- **Bad feedback is worse than none.** ~1/3 of feedback interventions *lower*
  performance (§2, Kluger & DeNisi 1996); self/ego-focused feedback is the
  classic failure mode.
- **Far transfer from gaming to cognition does not happen** (Oei & Patterson,
  2017, Psychol. Bull., DOI 10.1037/bul0000139 — video-game training does not
  enhance general cognitive ability). Implication: don't market "your brain gets
  faster"; market *game-specific decision skill*, which is what actually
  transfers (to the game).
- **"Mindset" / motivational pep-talk interventions do not reliably work.**
  A meta-analysis of growth-mindset interventions (Sisk et al., 2018/2022,
  Psychol. Bull., DOI 10.1037/bul0000352; 63 studies, N=97,672) found the average
  effect on achievement **≈ 0.02 (95% CI [-0.06, 0.10]) — null**, with apparent
  effects attributable to design flaws/bias. (A separate national experiment,
  Yeager et al., 2019, Nature, DOI 10.1038/s41586-019-1466-y, found gains only
  for **lower-achieving students under aligned peer norms**.) **Implication:**
  the product's value must be *concrete, corrective information* (§2), not
  inspiration or mindset content. **confidence: High.**

**Gaps (mark as unresolved):**
- **[partial] No LoL-specific RCT of VOD review vs no review exists** in the
  reachable literature. All effect sizes are borrowed from adjacent domains.
  `confidence: Low` for any specific "X% rank gain from VOD review."
- **No public study links *review behaviour* (e.g. reviews-per-week) to *MMR
  change*.** The product can and should generate this itself.
- **Community "coaching works" claims** (Reddit/YouTube/coaching sites) are
  expert opinion, `confidence: Low`, and were not required here.
- **No LoL-specific study of AI-generated review** exists; the closest prior art
  is the LoL win-prob analytics work (§6), which does not measure behavioural
  outcomes.

---

## 8. Design implications for an automated AI VOD-review tool

Distilled, each traced to the evidence above:

1. **Make the review a *retrieval test*, not a highlight reel** (§5). Ask the
   player to predict/justify the decision at key timestamps *before* revealing
   the model answer.
2. **Supply the objective reference standard** (§4). The AI's job is the
   comparison the player cannot make alone.
3. **One primary message per review, task-focused, actionable, with a concrete
   fix** (§2). Avoid ego/self framing; avoid stat spam (§6).
4. **Spaced, recurring "mistake-class" drills** (§5), not one-off per-game
   reports — retrieve the *same class of error* across multiple games/days.
5. **External, outcome-based framing** ("the objective was free at 0:42") over
   internal/mechanical framing (§2, OPTIMAL theory).
6. **Small, role-anchored metric set with a model answer**, jungle-specific
   (§6).
7. **Measure your own effect**: log review-behaviour vs MMR/win-rate change to
   create the LoL-specific evidence that the literature lacks (§7).
8. **Treat tilt as a first-class input** (§6b): a loss-framed stat dump *raises*
   tilt risk, and tilt-risk rises with anger and hours played. Frame each review
   as forward-looking and controllable; optionally surface emotion-regulation
   prompts.
9. **Don't sell mindset/motivation; sell corrective information** (§7). Mindset
   interventions are null on average (d≈0.02); task-focused feedback is d≈0.4–0.5.

---

## Sources (all fetched 2026-09-24 via OpenAlex/Crossref-indexed metadata)

1. Ericsson, Krampe & Tesch-Römer (1993). *The role of deliberate practice…*
   Psychol. Rev. 100(3):363. DOI 10.1037/0033-295x.100.3.363.
2. Macnamara, Hambrick & Oswald (2014). *Deliberate Practice and Performance in
   Music, Games, Sports, Education, and Professions: A Meta-Analysis.* Psychol.
   Sci. DOI 10.1177/0956797614535810 (+ corrigendum 2018 DOI
   10.1177/0956797618769891).
3. Ericsson (2019). *Deliberate Practice and Proposed Limits…* Front. Psychol.
   DOI 10.3389/fpsyg.2019.02396.
4. Wisniewski, Zierer & Hattie (2020). *The Power of Feedback Revisited: A
   Meta-Analysis of Educational Feedback Research.* Front. Psychol. DOI
   10.3389/fpsyg.2019.03087.
5. Kluger & DeNisi (1996). *The effects of feedback interventions on performance.*
   Psychol. Bull. 119(2):254.
6. *Practice Feedback Interventions: 15 Suggestions* (2016). Ann. Intern. Med.
   DOI 10.7326/m15-2248.
7. Wulf & Lewthwaite (2016). *OPTIMAL theory of motor learning.* Psychon. Bull.
   Rev. DOI 10.3758/s13423-015-0999-9.
8. Sigrist et al. (2012). *Augmented feedback in motor learning: a review.*
   Psychon. Bull. Rev. DOI 10.3758/s13423-012-0333-8.
9. Boyer et al. (2009). *Video modeling by experts with video feedback to enhance
   gymnastics skills.* JABA 42:855. DOI 10.1901/jaba.2009.42-855.
10. Morales et al. (2013). *Effectiveness of a Video-Feedback and Questioning
    Programme to Develop Cognitive Expertise in Sport.* PLoS ONE 8(12):e82270.
    DOI 10.1371/journal.pone.0082270.
11. Panadero, Jonsson & Botella (2017). *Effects of self-assessment on
    self-regulated learning and self-efficacy: Four meta-analyses.* Educ. Res.
    Rev. DOI 10.1016/j.edurev.2017.08.004.
12. Dunning (2017). *Dunning–Kruger effects in reasoning…* Psychon. Bull. Rev.
    DOI 10.3758/s13423-017-1242-7.
13. Nicol (2020). *The power of internal feedback…* Assess. Eval. High. Educ.
    DOI 10.1080/02602938.2020.1823314.
14. Winstone et al. (2016). *Supporting Learners' Agentic Engagement With
    Feedback.* Educ. Psychol. DOI 10.1080/00461520.2016.1207538.
15. Cepeda et al. (2006). *Distributed practice in verbal recall tasks.* Psychol.
    Bull. 132(3):354. DOI 10.1037/0033-2909.132.3.354.
16. Donoghue & Hattie (2021). *A Meta-Analysis of Ten Learning Techniques.*
    Front. Educ. DOI 10.3389/feduc.2021.581216.
17. *Avoiding Surgical Skill Decay: … Spacing of Training Sessions* (2017).
    J. Surg. Educ. DOI 10.1016/j.jsurg.2017.08.002.
18. Kari & Karhulahti (2020). *The structure of performance and training in
    esports.* PLoS ONE. DOI 10.1371/journal.pone.0237584.
19. *Cognitive expertise in esport experts: a three-level model meta-analysis*
    (2024). PeerJ. DOI 10.7717/peerj.17857.
20. Doğan et al. (2020). *Performance analysis in esports: modelling performance
    at the 2018 LoL World Championship.* Int. J. Sports Sci. Coaching. DOI
    10.1177/1747954120932853.
21. *Smart kills and worthless deaths: eSports analytics for League of Legends*
    (2020). J. Quant. Anal. Sports. DOI 10.1515/jqas-2019-0096.
22. *E-Sports Player Performance Metrics… Considering Player Roles* (2023). SN
    Comput. Sci. DOI 10.1007/s42979-022-01660-6.
23. *Esports Training, Periodization, and Software—A Scoping Review* (2024).
    Appl. Sci. DOI 10.3390/app142210354.
24. *Stress and Coping in Esports and the Influence of Mental Toughness* (2020).
    Front. Psychol. DOI 10.3389/fpsyg.2020.00628.
25. Oei & Patterson (2017). *Video game training does not enhance cognitive
    ability.* Psychol. Bull. DOI 10.1037/bul0000139.
26. *The psychology of esports: Trends, challenges, and future directions*
    (2025). Psychol. Sport Exerc. DOI 10.1016/j.psychsport.2025.102967.
27. Sisk et al. (2018/2022). *Do growth mindset interventions impact students'
    academic achievement?* Psychol. Bull. DOI 10.1037/bul0000352.
28. Yeager et al. (2019). *A national experiment reveals where a growth mindset
    improves achievement.* Nature. DOI 10.1038/s41586-019-1466-y.
29. *Playing for keeps or just playing with emotion? Studying tilt and emotion
    regulation in video games* (2024). Front. Psychol. DOI
    10.3389/fpsyg.2024.1385242.
30. *Playing with Emotions: A Systematic Review Examining Emotions and Emotion
    Regulation in Esports Performance* (2023). ACM. DOI 10.1145/3611041.
31. *Stressors and coping strategies in esports: a systematic review* (2024).
    DOI 10.1080/1750984x.2024.2386528.
32. Charleer et al. (2018). *Real-Time Dashboards to Support eSports Spectating.*
    ACM. DOI 10.1145/3242671.3242680.
33. Winstone et al. (2016) & Nicol (2020) — see items 13–14.
