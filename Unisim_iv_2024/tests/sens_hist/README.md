Original history file is quite difficult to read, a few changes were proposed:

* Replace TIME with DATE (mod0).
    * No changes in the results.
* Remove the additional TIMEs (mod1).
    * No changes in the results.
    * No need to change well rates 0.01 days before the actual date it should change, and then the *right* date is shown right after the TARGET keyword. This was done merely to improve plotting in Results.
    * Stair-steps option in Results doesn't properly print the historical rates.
* Group TARGET keywords whenever possible (mod2).
    * No changes in the results, but material balance was slightly worse and runtime a bit worse.
        * Not sure why the performance changed, since the information inserted into the simulator is the same (as mod1).
        * Runtime change is probably associated to server used in the simulation.
    * Added a DTWELL of 0.01 in mod2a.
        * This addition reduced the runtime to the same level as the other (mod 0 and 1).
* Reversed additional TIMEs removal (mod3).
    * Since simulation time is the same and the plots are worse when the additional TIMEs are removed, this modification was reversed.
    * **Decided** to continue with the mod3a version (changes TIME to DATE + group TARGET + DTWELL 0.01)
