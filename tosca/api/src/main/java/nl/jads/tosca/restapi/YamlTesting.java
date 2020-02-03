package nl.jads.tosca.restapi;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

import java.io.File;

public class YamlTesting {
    public static void main(String[] args) {
        ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
        try {
            TOSCADef toscaDef = mapper.readValue(
                    new File("C:\\Postdoc\\projects\\sodalite-eu\\defect-prediction\\tosca\\core\\src\\test\\resources\\hpc-clinical-uc\\service.yml"), TOSCADef.class);
            System.out.println(toscaDef.getMetadata().getTemplateName());
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
