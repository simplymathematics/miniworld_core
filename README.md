# MiniWorld Core

## Demo

A short demo shows 3 KVM OpenWRT nodes with B.A.T.M.A.N. advanced routing:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/j6D-43Tso04/0.jpg)](https://youtu.be/j6D-43Tso04?list=PLU2J7CyV0Bom-gBxH_NdKPX8jfrQDtS5v)

Another [video](https://youtu.be/6VG-qg2IhgM?list=PLU2J7CyV0Bom-gBxH_NdKPX8jfrQDtS5v) shows the `RandomWalk` movement pattern.

## About
MiniWorld (Mobile Infrastructure'n'Network Integrated World) enables network emulation in Linux.

Distributed applications, routing algorithms, etc. can be tested with MiniWorld.

For that purpose, the software-under-test has to be deployed in a KVM VM. Afterwards, the VMs can be interconnected by a network backend. For each connection, different static or event-based link-impairment can be applied. The network topology changes with a step.

## Features
- Network emulation with Linux Bridges and VDE
	- Wired and wireless link emulation
	- Network Supervision
	- Differential Network Switching
- QEMU/KVM node virtualization
    - Copy on write (COW) for VM images
    - Snapshot boot mode to speed up similar emulation runs
    - Node provisioning via serial shell (no SSH required)
    - Emulate arbitrary system architectures with QEMU
    - Node RAM Disk and COW reduces Disk I/O
- Distributed mode based on [ZeroMQ](http://zeromq.org)
    - GRE Tap tunnels to interconnect Emulation Servers
- Movement Patterns such as RandomWalk and [CORE](https://www.nrl.navy.mil/itd/ncs/products/core) integration
- Basic Link Quality Models based on Linux HTB and netem

## Documentation

We are currently creating the API documentation for MiniWorld on [readthedocs](http://miniworld-core.readthedocs.io/en/nightly/). Until the documentation is fully ready, please use the nightly branch.
The API documentation introduces MiniWorld from a user perspective.

For more information about the technical details you should read the paper or even the master thesis (for a very detailed documentation).

- [Master Thesis](https://github.com/miniworld-project/miniworld_core/blob/nightly/doc/master_thesis_nils_schmidt.pdf)
- Paper: Link following if paper is published

## Contribute
MiniWorld is an open-source project.
Do you have some good ideas, improvements, or even want to get your hands dirty?
There is a lot of work in the backlog and we can assign you small issues such that you can have a closer look at the source code.
Do not hesitate to contact us!

## Backlog
- Documentation
- More advanced scenario editor (currently: CORE)
- High-fidelity link-emulation (integrate with ns-3?)
- Android-based emulation with location (lat/lon) set via adb
- Lightweight virtualization for cases where full-system virt. is not needed
- Web UI
