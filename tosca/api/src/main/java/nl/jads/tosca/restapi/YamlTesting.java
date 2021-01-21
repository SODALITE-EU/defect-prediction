package nl.jads.tosca.restapi;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

import java.io.File;
import java.util.logging.Logger;

public class YamlTesting {
    private static final java.util.logging.Logger log = Logger.getLogger(YamlTesting.class.getName());

    public static void main(String[] args) {
        ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
        try {
            TOSCADef toscaDef = mapper.readValue(
                    new File("C:\\Postdoc\\projects\\sodalite-eu\\defect-prediction\\tosca\\core\\src\\test\\resources\\hpc-clinical-uc\\service.yml"), TOSCADef.class);
            System.out.println(toscaDef.getMetadata().getTemplateName());
        } catch (Exception e) {
            log.warning(e.getMessage());
        }
    }
}
