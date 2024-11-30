import http from '../http-common'

class CompetitionService {
  getAll () {
    return http.get('/api/v1/competitions')
      .then((res) => {
        return res
      })
  }
}

export default new CompetitionService()
