GALXE_API_URL = "https://graphigo.prd.galaxy.eco/query"


QUERIES = {
    "Cred": {
        "name": "Cred",
        "query": """query  Cred($id: ID!, $eligibleAddress: String!) {
  credential(id: $id, eligibleAddress: $eligibleAddress) {
    id
    name
    credType
    credSource
    curatorSpace {
      id
      alias
      name
      isVerified
      thumbnail
      isAdmin(address: $eligibleAddress)
      __typename
    }
    referenceLink
    description
    chain
    lastUpdate
    syncRate
    syncStatus
    lastSyncedBlock
    eligible(address: $eligibleAddress)
    itemCount
    subgraph {
      endpoint
      query
      expression
      __typename
    }
    credVersion
    lastSync
    multiDimensionCredConfig {
      ...MultiDimensionCred
      __typename
    }
    credValueSchema
    credValueData
    metadata {
      ...FullCredMetaData
      __typename
    }
    value {
      address
      campaignReferral {
        count
        __typename
      }
      gitcoinPassport {
        score
        lastScoreTimestamp
        __typename
      }
      walletBalance {
        balance
        __typename
      }
      multiDimension {
        value
        __typename
      }
      __typename
    }
    commonInfo {
      seoImage
      __typename
    }
    recurrence
    credQuiz {
      quizzes {
        title
        type
        items {
          value
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment MultiDimensionCred on MultiDimensionCredConfig {
  dataType
  dataSource
  contractAddress
  dataTags
  abiBytes
  handlerType
  aggregatorDetail
  updaterDetail
  handlerPeriodType
  handlerEndBlock
  handlerEndTimestamp
  subscriberCount
  dataSchema
  dataDefaultValue
  __typename
}

fragment FullCredMetaData on CredMetadata {
  ...CredMetaData
  survey {
    ...SurveyCredMetadataFrag
    __typename
  }
  __typename
}

fragment CredMetaData on CredMetadata {
  visitLink {
    link
    __typename
  }
  gitcoinPassport {
    score {
      title
      type
      description
      config
      __typename
    }
    lastScoreTimestamp {
      title
      type
      description
      config
      __typename
    }
    __typename
  }
  campaignReferral {
    count {
      title
      type
      description
      config
      __typename
    }
    __typename
  }
  galxeScore {
    dimensions {
      id
      type
      title
      description
      config
      values {
        name
        type
        value
        __typename
      }
      __typename
    }
    __typename
  }
  twitter {
    twitterID
    campaignID
    isAuthentic
    __typename
  }
  restApi {
    url
    method
    headers {
      key
      value
      __typename
    }
    postBody
    expression
    __typename
  }
  walletBalance {
    contractAddress
    snapshotTimestamp
    chain
    balance {
      type
      title
      description
      config
      __typename
    }
    LastSyncBlock
    LastSyncTimestamp
    __typename
  }
  lensProfileFollow {
    handle
    __typename
  }
  graphql {
    url
    query
    expression
    __typename
  }
  lensPostUpvote {
    postId
    __typename
  }
  lensPostMirror {
    postId
    __typename
  }
  multiDimensionRest {
    url
    method
    headers {
      key
      value
      __typename
    }
    postBody
    expression
    dimensions {
      id
      type
      title
      description
      config
      __typename
    }
    __typename
  }
  multiDimensionGraphql {
    url
    query
    expression
    dimensions {
      id
      type
      title
      description
      config
      __typename
    }
    __typename
  }
  contractQuery {
    url
    chainName
    abi
    method
    headers {
      key
      value
      __typename
    }
    contractMethod
    contractAddress
    block
    inputData
    inputs {
      name
      type
      value
      __typename
    }
    dimensions {
      id
      type
      config
      description
      title
      __typename
    }
    __typename
  }
  __typename
}

fragment SurveyCredMetadataFrag on SurveyCredMetadata {
  surveies {
    title
    type
    items {
      value
      __typename
    }
    __typename
  }
  __typename
}
"""
    }
}

CAMPAIGNS = {
    "Quest Four - Aptos Ecosystem Fundamentals": {
        "name": "Quest Four - Aptos Ecosystem Fundamentals",
        "credentials": {
            "On-Chain Task Verification": {
                "name": "On-Chain Task Verification",
                "id": "393089378257244160",
            }
        }
    }
}
