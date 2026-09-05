# Broken variant: no replan budget

## What's different

`max_replans` is removed from the schema entirely, and the failure branch always calls `Replan_Remaining` no matter how many times it's already failed.

## Why this breaks in practice

If the underlying reason a step keeps failing is structural (e.g. the task asks for data from a source that doesn't exist), the model will happily generate a new plan every time, and the loop only terminates when the Until action's own hard count limit kicks in — burning a full budget's worth of model calls to arrive at the same place a `max_replans: 2` cap would have reached in three. Worse, because each replan call succeeds (it's the *executed* step that fails, not the planning call), nothing about this looks broken from the outside until you check the token bill or the run duration.

## The fix

`max_replans` plus the explicit "give up and record stopped_reason" branch in the working version's step 6 is what turns an unbounded retry-via-replanning loop into a tool with a knowable worst case.

## Fill this in once tested

Once built, replace this with the actual iteration count and cost difference observed between the capped and uncapped versions on a deliberately-unsolvable task.
