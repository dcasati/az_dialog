# Azure Resource Group Cleaner

This is a small dialog-based program that will allow for the batch deletion of resource groups in Azure.

![asciicast](demo.gif)

1. Run the container:

```bash
docker run -it --rm -v ${HOME}/.azure:/root/.azure dcasati/az_dialog:latest
```

1. Select the resources to be deleted
1. Hit 'ok' to delete the resources.

To verify the statuses of the resource groups, navigate to the main menu and select `List Resource Groups`
