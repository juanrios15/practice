/** @jsx jsx */
/** @jsxRuntime classic */
import React, { useState, useEffect } from 'react';
import axios from "axios";
import { jsx } from '@emotion/react';

// Local 
import Box from '../../components/box';
import Text from '../../components/text';
import Card from '../../components/cards';
import TopMenu from '../../components/topMenu';

// Styles
import * as styles from './styles';
import { CardsGrid } from './styles';

//Utils
import { splitName } from '../../utils/splitName';
import { convertUnixToTime } from '../../utils/converUnixToTime';

// Change Request Time to API in Milliseconds
const requestTimeMilliseconds = 15000;

const endpoints = [
  "https://api.factoryfour.com/accounts/health/status",
  "https://api.factoryfour.com/assets/health/status",
  "https://api.factoryfour.com/customers/health/status",
  "https://api.factoryfour.com/datapoints/health/status",
  "https://api.factoryfour.com/devices/health/status",
  "https://api.factoryfour.com/documents/health/status",
  "https://api.factoryfour.com/forms/health/status",
  "https://cors-anywhere.herokuapp.com/https://api.factoryfour.com/invites/health/status",
  "https://api.factoryfour.com/media/health/status",
  // "https://api.factoryfour.com/messages/health/status",
  "https://api.factoryfour.com/namespaces/health/status",
  "https://api.factoryfour.com/orders/health/status",
  "https://api.factoryfour.com/patients/health/status",
  "https://api.factoryfour.com/relationships/health/status",
  "https://api.factoryfour.com/rules/health/status",
  "https://api.factoryfour.com/templates/health/status",
  // "https://api.factoryfour.com/users/health/status",
  "https://api.factoryfour.com/workflows/health/status",
]

const instance = axios.create({
  baseURL: 'https://api.factoryfour.com/',
  timeout: 1000,
  headers: {'Access-Control-Allow-Origin': '*'}
});

instance.interceptors.response.use(function (config) {
  return config
  }, function (error) {

  });

const Home = () => {
  const [apiData, setApiData] = useState([]);
  const [showError, setShowError] = useState();

  const getData = () => {
    Promise.all(endpoints.map((endpoint) => instance.get(endpoint)))
      .then((data) => {
        setApiData(data)
        console.log('API-DATA:', data)
      })
      .catch(err => {
        setShowError(err.message);
      });
  }

  // const getData = async () => {
  //   try {
  //     console.log("Processing...");
  //     const request = endpoints.map((endpoint) => axios.get(endpoint));
  //     const data = await request.json();
  //     return setApiData(data);
  //   } catch (err) {
  //     setShowError(err.message);
  //   }

  // };

  // console.log(showError)

  useEffect(() => {
    getData();
    const intv = setInterval(getData, requestTimeMilliseconds);
    return () => clearInterval(intv);
  }, []);

  return (
    <>
      <Box
        className="container"
        flexDirection="row"
        justifyContent="center"
        css={styles.container}
      >
        <TopMenu>
          <Box>
            <Text
              color="white"
              fontSize="30px"
              fontWeight="bold"
            >
              STATUS DASHBOARD
            </Text>
          </Box>
        </TopMenu>
        <Box mt="5%" mb="5%" justifyContent="center">
          <CardsGrid>
            {apiData.map((card, index) => (
              card!=undefined &&
              <Box key={index}>
                <Card>
                  <Box>
                    <Text
                      color="white"
                      fontSize="25px"
                      fontWeight="bold"
                    >
                      {card.data && splitName(card.data.hostname, '-')}
                    </Text>
                  </Box>
                  <Box width="90%" margin="10px" padding="5px" 
                    bgColor={card.data.message.includes('Healthy') ? '#68dd97' : '#e53b3b'}
                  >
                    {splitName(card.data.message, ':')}
                  </Box>
                  <Box>
                    <Text
                      color="white"
                      fontSize="15px"
                    >
                      {card.data.hostname}
                    </Text>
                  </Box>
                  <Box>
                    <Text
                      color="white"
                      fontSize="15px"
                    >
                      {convertUnixToTime(card.data.time)}
                    </Text>
                  </Box>
                </Card>
              </Box>
            ))}
          </CardsGrid>
        </Box>

      </Box>

    </>
  );
}

export default Home;
