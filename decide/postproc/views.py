from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return out

    def borda(self, options):
        out = []

        for opt in options:
            votes = 0
            options_number = len(options)
            for i in range(0, options_number):
                votes += opt['votes'][i]*(options_number-i)
            out.append({
                **opt,
                'postproc': votes,
            })

        out.sort(key=lambda x: -x['postproc'])
        return out

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        out = []
        questions = request.data

        for q in questions:
            t = q['type']
            opts = q['options']
            if t == 'IDENTITY':
                out.append(self.identity(opts))
            if t == 'BORDA':
                out.append(self.borda(opts))

        return Response(out)
