// Shared hosting for every Logic Apps MCP tool artifact in this repo.
//
// Why one shared Standard Logic App instead of one per tool: MCP-server
// hosting requires the Standard tier (Workflow Service Plan), which is
// billed hourly — unlike Consumption, which is pay-per-execution. Microsoft's
// own docs recommend grouping multiple MCP servers/workflows inside a single
// Standard logic app, and doing so here means you pay for ONE hourly-billed
// plan across every artifact in this repo, not one per tool.
//
// Cost shape at deploy time (approximate, verify current pricing before you
// rely on this): WS1 Workflow Service Plan is billed per vCPU/memory-hour,
// roughly on the order of $0.20-$0.40/hour depending on region — a few hours
// of testing is a couple of dollars, not a recurring bill, AS LONG AS you
// tear the resource group down when you're done (see README in this folder).
// The storage account and Application Insights are both consumption-priced
// and effectively free at the transaction volumes a solo dev generates.
//
// NOTE: this template has not been live-deployed by the assistant that wrote
// it (no Azure access here) — run `az deployment group validate` before
// `az deployment group create`, and treat the first real deploy as a test.
// If it errors, that error is exactly the kind of thing this repo's
// failure-first docs exist to capture — fix it, then add it to docs/failures/.

@description('Prefix used to name every resource. Keep it short, lowercase, alphanumeric.')
@minLength(3)
@maxLength(16)
param namePrefix string = 'agenticplumb'

@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('Workflow Service Plan SKU. WS1 is the smallest/cheapest Standard tier that supports MCP server hosting.')
@allowed([
  'WS1'
  'WS2'
  'WS3'
])
param workflowPlanSku string = 'WS1'

var storageAccountName = toLower('${namePrefix}st${uniqueString(resourceGroup().id)}')
var appServicePlanName = '${namePrefix}-plan'
var logicAppName = '${namePrefix}-mcp-host'
var appInsightsName = '${namePrefix}-ai'
var contentShareName = toLower('${namePrefix}-content')

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    IngestionMode: 'ApplicationInsights'
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  kind: 'elastic'
  sku: {
    name: workflowPlanSku
    tier: 'WorkflowStandard'
  }
  properties: {
    maximumElasticWorkerCount: 5
  }
}

resource logicApp 'Microsoft.Web/sites@2023-12-01' = {
  name: logicAppName
  location: location
  kind: 'functionapp,workflowapp'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=${environment().suffixes.storage}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=${environment().suffixes.storage}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: contentShareName
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'node'
        }
        {
          name: 'WEBSITE_NODE_DEFAULT_VERSION'
          value: '~18'
        }
        {
          name: 'APP_KIND'
          value: 'workflowApp'
        }
        {
          name: 'AzureFunctionsJobHost__extensionBundle__id'
          value: 'Microsoft.Azure.Functions.ExtensionBundle.Workflows'
        }
        {
          name: 'AzureFunctionsJobHost__extensionBundle__version'
          value: '[1.*, 2.0.0)'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
      ]
      netFrameworkVersion: 'v6.0'
    }
  }
}

output logicAppName string = logicApp.name
output logicAppHostname string = logicApp.properties.defaultHostName
output storageAccountName string = storageAccount.name
output appInsightsName string = appInsights.name
